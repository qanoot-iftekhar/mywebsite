from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Category, Product, Cart, Order, OrderItem, 
    Review, NewsletterSubscription, Page, SocialMediaLink
)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model with category details"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'category', 
            'category_name', 'category_slug', 'image', 'featured', 
            'rating', 'created_at'
        ]
        read_only_fields = ['created_at']


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for Cart items with product details"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = [
            'id', 'product', 'product_name', 'product_price', 
            'product_image', 'quantity', 'size', 'color', 'subtotal', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']
    
    def get_subtotal(self, obj):
        return obj.product.price * obj.quantity


class CartCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating cart items"""
    class Meta:
        model = Cart
        fields = ['product', 'quantity', 'size', 'color']
    
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value



class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for Order items"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model with items"""
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'total_amount', 'status', 'created_at',
            'full_name', 'email', 'phone', 'address', 'city', 'state', 
            'zip_code', 'items'
        ]
        read_only_fields = ['user', 'order_number', 'created_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders"""
    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone', 'address', 
            'city', 'state', 'zip_code'
        ]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'user_name', 'product', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']

class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = ['id', 'email', 'created_at']
        read_only_fields = ['created_at']

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['slug', 'title', 'content', 'updated_at']

class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = ['platform', 'url', 'icon']
