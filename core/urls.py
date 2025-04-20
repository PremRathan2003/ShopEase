from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    
    # Admin dashboard
    path('dashboard/admin/', views.admin_index, name='admin_index'),
    
    # Product-related URLs
    path('products', views.products, name='products'),  # View all products
    path('products/ease', views.admin_products, name='admin_products'),  # Admin view for managing products
    
    # Add new product
    path('products/add', views.add_product, name='add_product'),
    
    # Delete a product
    path('products/<int:id>/delete/', views.delete_product, name='delete_product'),
    
    # Product search
    path('products/search', views.search_products, name='search_products'),  # User-side search for products
    path('products/search/ease', views.admin_search_products, name='admin_search_products'),  # Admin-side product search
    
    # Static pages
    path('about', views.about, name='about'),  # About page
    path('contact', views.contact, name='contact'),  # Contact page
    
    # Message-related URLs
    path('send/message', views.send_message, name='send_message'),  # Send a new message
    path('messages/', views.view_messages, name='messages'),  # View all messages
    path('update/message/<int:id>/', views.update_message, name='update_message'),  # Update a specific message
    path('message/<int:pk>/delete/', views.delete_message, name='delete_message'),  # Delete a message
    path('mark-as-read/<int:pk>/', views.mark_as_read, name='mark_as_read'),  # Mark message as read
    path('message/admin/', views.admin_messages, name='admin_messages'),  # Admin view of messages
    
    # Order-related URLs
    path('order/success/', views.order_success, name='order_success'),  # Success page after placing an order
    path('checkout/', views.checkout_view, name='checkout'),  # Checkout page
    path('orders/', views.orders, name='orders'),  # View all orders
    path('update/<int:pk>/order', views.update_order, name='update_order'),  # Update order details
    path('orders/ease', views.admin_orders, name='admin_orders'),  # Admin view of orders
    path('complete/order/<int:pk>/ease', views.complete_order, name='complete_order'),  # Mark order as complete
    
    # Authentication-related URLs
    path('logout/', views.logout_view, name='logout'),  # Log out
    path('login/', views.login_view, name='login'),  # Log in
    path('register', views.register_user, name='register_user'),  # User registration
    
    # Product-specific URLs
    path('product/<int:pk>/get/', views.get_product_data, name='get_product_data'),  # Get product data by ID
    path('product/<int:pk>/update/', views.update_product, name='update_product'),  # Update product details
    
    # Admin superuser creation
    path('create-superuser/', views.create_superuser, name='create_superuser'),  # Create superuser for the admin
    
]

# Serving media files during development (if needed)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
