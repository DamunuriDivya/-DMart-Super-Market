from django.urls import path
from . import views

urlpatterns = [
    # Home and Products
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),

    # Cart URLs
    path('add-to-cart/<str:product_name>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),

    # Login and Registration
   
path('login/', views.login_page, name='login'),
path('register/', views.register_page, name='register'),
path('logout/', views.logout_page, name='logout'),
path('profile/', views.profile_page, name='profile'),

    # Wishlist URLs
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_page, name='wishlist'),
    path('remove-wishlist/<int:id>/', views.remove_wishlist, name='remove_wishlist'),
       # Payment URLs
    path('payment/', views.payment_page, name='payment'),
    path('process-payment/', views.process_payment, name='process_payment'),

    # Order Confirmation URL
    path('confirm-order/', views.confirm_order, name='confirm_order'),
    path('remove-from-cart/<str:product_name>/', views.remove_from_cart, name='remove_from_cart'),
]