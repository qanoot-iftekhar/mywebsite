from rest_framework import generics, filters, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Product, Category, Cart
from .serializers import ProductSerializer, CategorySerializer, CartCreateSerializer

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'featured']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Custom price filtering
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Size filtering
        size = self.request.query_params.get('size')
        if size:
            queryset = queryset.filter(variants__size=size).distinct()
        
        # Color filtering
        color = self.request.query_params.get('color')
        if color:
            queryset = queryset.filter(variants__color=color).distinct()
            
        return queryset

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class CartAPIView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CartCreateSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
            size = serializer.validated_data.get('size', '')
            color = serializer.validated_data.get('color', '')
            
            if request.user.is_authenticated:
                # Database Cart for Logged-in Users
                cart_item, created = Cart.objects.get_or_create(
                    user=request.user,
                    product=product,
                    size=size,
                    color=color,
                    defaults={'quantity': quantity}
                )
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
            else:
                # Session Cart for Anonymous Users
                cart = request.session.get('cart', {})
                # Create a unique key for product + size + color
                item_key = f"{product.id}_{size}_{color}"
                
                if item_key in cart:
                    cart[item_key]['quantity'] += quantity
                else:
                    cart[item_key] = {
                        'product_id': product.id,
                        'quantity': quantity,
                        'size': size,
                        'color': color
                    }
                
                request.session['cart'] = cart
                request.session.modified = True
                
            return Response({'status': 'success', 'message': 'Product added to cart'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        size = request.data.get('size', '')
        color = request.data.get('color', '')
        
        if not product_id or quantity is None:
            return Response({'error': 'Product ID and quantity required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            quantity = int(quantity)
            if quantity < 1:
                return Response({'error': 'Quantity must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
             return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_authenticated:
            try:
                # Find item by product, size, and color
                cart_item = Cart.objects.get(
                    user=request.user, 
                    product_id=product_id,
                    size=size,
                    color=color
                )
                cart_item.quantity = quantity
                cart_item.save()
            except Cart.DoesNotExist:
                return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)
        else:
            cart = request.session.get('cart', {})
            item_key = f"{product_id}_{size}_{color}"
            
            # Fallback for old session structure (just product_id)
            if item_key not in cart and str(product_id) in cart:
                item_key = str(product_id)

            if item_key in cart:
                if isinstance(cart[item_key], dict):
                    cart[item_key]['quantity'] = quantity
                else:
                    # Handle legacy simple int quantity
                    cart[item_key] = quantity
                    
                request.session['cart'] = cart
                request.session.modified = True
            else:
                return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'status': 'success', 'message': 'Cart updated'}, status=status.HTTP_200_OK)

    def get(self, request):
        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=request.user)
            from .serializers import CartItemSerializer
            serializer = CartItemSerializer(cart_items, many=True)
            return Response({'count': cart_items.count(), 'items': serializer.data})
        else:
            cart = request.session.get('cart', {})
            items = []
            
            for key, item_data in cart.items():
                # Handle both new dict structure and old int structure
                if isinstance(item_data, dict):
                    product_id = item_data['product_id']
                    quantity = item_data['quantity']
                    size = item_data.get('size', '')
                    color = item_data.get('color', '')
                else:
                    product_id = key
                    quantity = item_data
                    size = ''
                    color = ''
                
                try:
                    product = Product.objects.get(id=product_id)
                    items.append({
                        'product': product.id,
                        'product_id': product.id,
                        'product_name': product.name,
                        'product_price': float(product.price),
                        'product_image': product.image.url if product.image else None,
                        'quantity': quantity,
                        'size': size,
                        'color': color,
                        'subtotal': float(product.price) * quantity
                    })
                except Product.DoesNotExist:
                    continue
                    
            return Response({'count': len(items), 'items': items})

    def delete(self, request):
        product_id = request.data.get('product_id')
        size = request.data.get('size', '')
        color = request.data.get('color', '')
        
        if not product_id:
            return Response({'error': 'Product ID required'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_authenticated:
            Cart.objects.filter(
                user=request.user, 
                product_id=product_id,
                size=size,
                color=color
            ).delete()
        else:
            cart = request.session.get('cart', {})
            item_key = f"{product_id}_{size}_{color}"
            
            # Fallback for old session structure
            if item_key not in cart and str(product_id) in cart:
                item_key = str(product_id)
                
            if item_key in cart:
                del cart[item_key]
                request.session['cart'] = cart
                request.session.modified = True
        
        return Response({'status': 'success', 'message': 'Item removed'}, status=status.HTTP_200_OK)

