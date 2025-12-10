import re

# Read models.py
with open('main/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Update Cart model - make user nullable and add session_key
content = content.replace(
    'class Cart(models.Model):\n    user = models.ForeignKey(User, on_delete=models.CASCADE)',
    'class Cart(models.Model):\n    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)  # Optional for guests\n    session_key = models.CharField(max_length=40, null=True, blank=True)  # For guest carts'
)

# Update Order model - make user nullable, use SET_NULL, and add is_guest
content = content.replace(
    '    user = models.ForeignKey(User, on_delete=models.CASCADE)\n    order_number',
    '    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Optional for guests\n    is_guest = models.BooleanField(default=False)  # Track if this is a guest order\n    order_number'
)

# Write back
with open('main/models.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Models updated successfully!")
print("- Cart: user is now optional, added session_key")
print("- Order: user is now optional, added is_guest field")
