from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')  # Main image
    featured = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Footwear specific fields
    material = models.CharField(max_length=100, blank=True, help_text="e.g., Leather, Canvas, Mesh")
    sole_type = models.CharField(max_length=100, blank=True, help_text="e.g., Rubber, EVA")
    weight = models.CharField(max_length=50, blank=True, help_text="e.g., 250g per shoe")
    is_water_resistant = models.BooleanField(default=False)
    care_instructions = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    def get_available_colors(self):
        """Returns list of unique colors available for this product"""
        return ProductVariant.objects.filter(product=self).values_list('color', flat=True).distinct()
    
    def get_available_sizes(self, color=None):
        """Returns available sizes, optionally filtered by color"""
        queryset = ProductVariant.objects.filter(product=self)
        if color:
            queryset = queryset.filter(color=color)
        return queryset.values_list('size', flat=True).distinct().order_by('size')

class ProductImage(models.Model):
    """Multiple images for a product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.product.name} - Image {self.order}"

class ProductVariant(models.Model):
    """Product variants for different color and size combinations"""
    SIZE_CHOICES = [
        ('6', 'UK 6'),
        ('7', 'UK 7'),
        ('8', 'UK 8'),
        ('9', 'UK 9'),
        ('10', 'UK 10'),
        ('11', 'UK 11'),
        ('12', 'UK 12'),
    ]
    
    COLOR_CHOICES = [
        ('black', 'Black'),
        ('white', 'White'),
        ('brown', 'Brown'),
        ('navy', 'Navy Blue'),
        ('grey', 'Grey'),
        ('beige', 'Beige'),
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.CharField(max_length=50, choices=COLOR_CHOICES)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True, help_text="Stock Keeping Unit")
    
    # Optional: Color-specific image
    color_image = models.ImageField(upload_to='products/colors/', blank=True, null=True)
    
    class Meta:
        unique_together = ['product', 'color', 'size']
        ordering = ['color', 'size']
    
    def __str__(self):
        return f"{self.product.name} - {self.get_color_display()} - {self.get_size_display()}"
    
    def is_in_stock(self):
        return self.stock > 0
    
    def is_low_stock(self):
        return 0 < self.stock <= 5

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)  # Optional for guests
    session_key = models.CharField(max_length=40, null=True, blank=True)  # For guest carts
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    # Variant information
    size = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Optional for guests
    is_guest = models.BooleanField(default=False)  # Track if this is a guest order
    order_number = models.CharField(max_length=20, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Shipping information
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=50, default='credit-card')

    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Variant information
    size = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Footwear-specific review fields
    TRUE_TO_SIZE_CHOICES = [
        ('small', 'Runs Small'),
        ('true', 'True to Size'),
        ('large', 'Runs Large'),
    ]
    
    WIDTH_CHOICES = [
        ('narrow', 'Too Narrow'),
        ('perfect', 'Perfect Width'),
        ('wide', 'Too Wide'),
    ]
    
    true_to_size = models.CharField(max_length=10, choices=TRUE_TO_SIZE_CHOICES, blank=True)
    width_feedback = models.CharField(max_length=10, choices=WIDTH_CHOICES, blank=True)
    comfort_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    would_recommend = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating})"

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Page(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class SocialMediaLink(models.Model):
    platform = models.CharField(max_length=50)
    url = models.URLField()
    icon = models.CharField(max_length=50, help_text="FontAwesome class, e.g., 'fab fa-facebook'")

    def __str__(self):
        return self.platform

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.name} - {self.city}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"