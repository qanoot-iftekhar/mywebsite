"""
Script to update views.py with guest checkout support
"""
import re

with open('main/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Read the new views
with open('views_guest_checkout.py', 'r', encoding='utf-8') as f:
    new_views = f.read()

# Extract the helper function and updated views
helper_function = '''def get_cart_items(request):
    """Helper function to get cart items for both logged-in and guest users"""
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).select_related('product', 'product__category')
    else:
        # Guest user - use session
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        return Cart.objects.filter(session_key=session_key).select_related('product', 'product__category')

'''

# Add random and string imports at the top
content = content.replace(
    'import json',
    'import json\nimport random\nimport string'
)

# Replace @login_required\ndef cart with new cart function (without @login_required)
# Find and replace the entire cart view
cart_pattern = r'@login_required\ndef cart\(request\):.*?return render\(request, \'cart\.html\', context\)'
cart_replacement = '''def cart(request):
    """Cart view - works for both logged-in and guest users"""
    cart_items = get_cart_items(request)
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart.html', context)'''

content = re.sub(cart_pattern, cart_replacement, content, flags=re.DOTALL)

# Replace @login_required\ndef add_to_cart
add_to_cart_pattern = r'@login_required\ndef add_to_cart\(request, product_id\):.*?return JsonResponse\(\{\'success\': False, \'message\': \'Invalid request\'\}\)'
add_to_cart_replacement = '''def add_to_cart(request, product_id):
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
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})'''

content = re.sub(add_to_cart_pattern, add_to_cart_replacement, content, flags=re.DOTALL)

# Replace @login_required\ndef checkout
checkout_pattern = r'@login_required\ndef checkout\(request\):.*?return render\(request, \'checkout\.html\', context\)'
checkout_replacement = '''def checkout(request):
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
    return render(request, 'checkout.html', context)'''

content = re.sub(checkout_pattern, checkout_replacement, content, flags=re.DOTALL)

# Add helper function after products view (around line 43)
# Find where to insert - after products view
insert_pos = content.find('def product_detail(request, product_id):')
if insert_pos > 0:
    content = content[:insert_pos] + helper_function + '\n' + content[insert_pos:]

with open('main/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Views updated successfully!")
print("- Removed @login_required from cart, add_to_cart, checkout")
print("- Added get_cart_items() helper function")  
print("- Added session cart support for guests")
print("- Updated checkout to handle guest orders")
