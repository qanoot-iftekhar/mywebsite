from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant, Cart, Order, OrderItem, Review, Address

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ['image', 'alt_text', 'order']

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 5
    fields = ['color', 'size', 'stock', 'sku', 'color_image']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'featured', 'rating', 'material']
    list_filter = ['category', 'featured', 'material']
    search_fields = ['name', 'description']
    inlines = [ProductImageInline, ProductVariantInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alt_text', 'order']
    list_filter = ['product']

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'color', 'size', 'stock', 'sku', 'is_in_stock']
    list_filter = ['color', 'size', 'product']
    search_fields = ['product__name', 'sku']
    list_editable = ['stock']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'size', 'color', 'quantity', 'created_at']
    list_filter = ['created_at', 'size', 'color']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username', 'email']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'size', 'color', 'quantity', 'price']
    list_filter = ['order', 'size', 'color']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'comfort_rating', 'true_to_size', 'would_recommend', 'created_at']
    list_filter = ['rating', 'true_to_size', 'width_feedback', 'would_recommend', 'created_at']
    search_fields = ['product__name', 'user__username', 'comment']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'city', 'state', 'zip_code', 'is_default']
    list_filter = ['is_default', 'state']
    search_fields = ['user__username', 'name', 'address_line1', 'city', 'zip_code']