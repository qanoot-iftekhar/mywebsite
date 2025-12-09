from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, Category, Cart, Order, OrderItem, Address, ProductVariant, Wishlist
from . import email_utils
import json
import random
import string

def home(request):
    featured_products = Product.objects.filter(featured=True)[:4]
    categories = Category.objects.all()
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'home.html', context)

def products(request):
    category_slug = request.GET.get('category')
    products = Product.objects.all()
    selected_category = None
    
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
            selected_category = category_slug
        except Category.DoesNotExist:
            # If category doesn't exist, just show all products
            pass
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'products.html', context)



def get_cart_items(request):
    """Helper function to get cart items for both logged-in and guest users"""
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).select_related('product', 'product__category')
    else:
        # Guest user - use session
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        return Cart.objects.filter(session_key=session_key).select_related('product', 'product__category')


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Get all variants for this product
    variants = product.variants.all()
    
    # Get unique colors available
    available_colors = product.get_available_colors()
    
    # Create variant data structure for JavaScript
    variant_data = {}
    for variant in variants:
        color = variant.color
        if color not in variant_data:
            variant_data[color] = {}
        
        variant_data[color][variant.size] = {
            'stock': variant.stock,
            'sku': variant.sku,
            'is_in_stock': variant.is_in_stock(),
            'is_low_stock': variant.is_low_stock(),
            'image': variant.color_image.url if variant.color_image else None
        }
    
    # Check if product is in wishlist
    is_in_wishlist = False
    if request.user.is_authenticated:
        is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    
    context = {
        'product': product,
        'available_colors': available_colors,
        'variants_json': json.dumps(variant_data),
        'is_in_wishlist': is_in_wishlist,
    }
    return render(request, 'product_detail.html', context)


def cart(request):
    """Cart view - works for both logged-in and guest users"""
    cart_items = get_cart_items(request)
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart.html', context)

def add_to_cart(request, product_id):
    """Add to cart - works for both logged-in and guest users"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if request.user.is_authenticated:
            # Logged-in user
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': quantity}
            )
        else:
            # Guest user - use session
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            
            cart_item, created = Cart.objects.get_or_create(
                session_key=session_key,
                product=product,
                defaults={'quantity': quantity}
            )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({'success': True, 'message': 'Product added to cart'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def checkout(request):
    """Checkout view - works for both logged-in and guest users"""
    cart_items = get_cart_items(request)
    
    if not cart_items:
        return redirect('cart')
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        # Combine first and last name
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        full_name = f"{first_name} {last_name}".strip()
        
        # Generate order number
        if request.user.is_authenticated:
            order_num_prefix = f"ORD-{request.user.id}"
            is_guest = False
            user = request.user
        else:
            # Guest order
            order_num_prefix = "ORD-GUEST"
            is_guest = True
            user = None
        
        order_number = f"{order_num_prefix}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
        
        # Process order
        order = Order.objects.create(
            user=user,
            is_guest=is_guest,
            order_number=order_number,
            total_amount=total,
            full_name=full_name,
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zip_code=request.POST.get('zip_code'),
            payment_method=request.POST.get('payment_method', 'credit-card'),
        )
        
        # Create order items and update stock
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                size=cart_item.size,
                color=cart_item.color
            )
            
            # Decrease stock for the specific variant
            try:
                variant = ProductVariant.objects.get(
                    product=cart_item.product,
                    size=cart_item.size,
                    color=cart_item.color
                )
                variant.stock -= cart_item.quantity
                variant.save()
            except ProductVariant.DoesNotExist:
                # If variant doesn't exist, skip stock update
                pass
        
        # Clear cart
        cart_items.delete()
        
        # Send order confirmation email
        try:
            email_utils.send_order_confirmation_email(order)
        except:
            pass  # Don't fail checkout if email fails
        
        return redirect('order_success', order_id=order.id)
    
    # Get user's saved addresses (only for logged-in users)
    addresses = []
    if request.user.is_authenticated:
        addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'addresses': addresses,
    }
    return render(request, 'checkout.html', context)

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'success.html', context)

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html')
            
        # Use email as username
        if User.objects.filter(username=email).exists():
            messages.error(request, 'An account with this email already exists')
            return render(request, 'signup.html')
            
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        # Send welcome email
        email_utils.send_welcome_email(user)
        
        login(request, user)
        return redirect('home')
        
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def men_page(request):
    """Dedicated page for men's jewelry collection"""
    return render(request, 'men.html')

def size_guide(request):
    """Size guide page for footwear sizing"""
    return render(request, 'size_guide.html')

@login_required
def profile(request):
    """User profile page with account management"""
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'profile':
            # Update profile
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name = request.POST.get('last_name', '')
            request.user.email = request.POST.get('email', '')
            request.user.save()
            messages.success(request, 'Profile updated successfully!')
            
        elif form_type == 'password':
            # Change password
            current_password = request.POST.get('current_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            
            if request.user.check_password(current_password):
                if new_password1 == new_password2:
                    request.user.set_password(new_password1)
                    request.user.save()
                    messages.success(request, 'Password changed successfully!')
                    return redirect('login')
                else:
                    messages.error(request, 'New passwords do not match!')
            else:
                messages.error(request, 'Current password is incorrect!')
        
        elif form_type == 'add_address':
            # Add new address
            is_default = request.POST.get('is_default') == 'on'
            
            # If setting as default, unset other defaults
            if is_default:
                Address.objects.filter(user=request.user).update(is_default=False)
                
            Address.objects.create(
                user=request.user,
                name=request.POST.get('name'),
                phone=request.POST.get('phone'),
                address_line1=request.POST.get('address_line1'),
                address_line2=request.POST.get('address_line2', ''),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                zip_code=request.POST.get('zip_code'),
                is_default=is_default
            )
            messages.success(request, 'Address added successfully!')
            
        elif form_type == 'delete_address':
            # Delete address
            address_id = request.POST.get('address_id')
            Address.objects.filter(id=address_id, user=request.user).delete()
            messages.success(request, 'Address deleted successfully!')
        
        return redirect('profile')
    
    # Get user's orders, addresses, and wishlist
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    
    context = {
        'orders': orders,
        'addresses': addresses,
        'wishlist_items': wishlist_items
    }
    return render(request, 'profile.html', context)

def contact(request):
    """Contact page"""
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # TODO: Send email or save to database
        messages.success(request, 'Thank you for contacting us! We will respond within 24 hours.')
        return redirect('contact')
    
    return render(request, 'contact.html')

def about(request):
    """About us page"""
    return render(request, 'about.html')

def return_policy(request):
    """Return and exchange policy page"""
    return render(request, 'return_policy.html')

@login_required
def toggle_wishlist(request, product_id):
    """Toggle product in user's wishlist"""
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
            wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
            
            if not created:
                # If item already exists, remove it
                wishlist_item.delete()
                action = 'removed'
            else:
                action = 'added'
                
            return JsonResponse({
                'status': 'success', 
                'action': action,
                'message': f'Product {action} to wishlist'
            })
            
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

