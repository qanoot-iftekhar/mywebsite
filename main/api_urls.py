from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    CategoryViewSet, ProductViewSet, CartViewSet, OrderViewSet, ReviewViewSet,
    register_user, login_user, logout_user, user_profile,
    newsletter_signup, page_detail, social_media_links
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', register_user, name='api-register'),
    path('auth/login/', login_user, name='api-login'),
    path('auth/logout/', logout_user, name='api-logout'),
    path('auth/profile/', user_profile, name='api-profile'),
    
    # New endpoints
    path('newsletter/', newsletter_signup, name='api-newsletter'),
    path('pages/<slug:slug>/', page_detail, name='api-page-detail'),
    path('social-media/', social_media_links, name='api-social-media'),
    
    # Router URLs
    path('', include(router.urls)),
]
