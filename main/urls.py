from django.urls import path
from . import views, api_views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
from django.urls import path
from . import views, api_views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('men/', views.men_page, name='men'),
    path('size-guide/', views.size_guide, name='size_guide'),
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('return-policy/', views.return_policy, name='return_policy'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    
    # OTP Authentication
    path('auth/request-otp/', views.request_email_otp, name='request_email_otp'),
    path('auth/verify-otp/', views.verify_email_otp, name='verify_email_otp'),
    path('login-otp/', views.login_with_otp, name='login_otp'),
    
    # API Endpoints
    path('api/products/', api_views.ProductListAPIView.as_view(), name='api_products'),
    path('api/categories/', api_views.CategoryListAPIView.as_view(), name='api_categories'),
    path('api/cart/', api_views.CartAPIView.as_view(), name='api_cart'),
]