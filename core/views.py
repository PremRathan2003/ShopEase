from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Product, Message, Order
from django.contrib import messages
from .forms import ProductForm
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login


# Logout the user and redirect to login page
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to your login page


# Register new users
def register_user(request):
    if request.method == 'POST':
        # Collect form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate the password and ensure it matches the confirmation
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register_user')

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register_user')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register_user')

        # Create the new user and save it to the database
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect('index')  # Redirect to the home page after registration

    return render(request, 'register.html')  # Return the registration page if the method is GET


# Display orders (only for logged-in users)
@login_required
def orders(request):
    context = {
        'orders': Order.objects.all()
    }
    return render(request, 'orders.html', context)


# Success page for orders
@login_required
def order_success(request):
    return render(request, 'success.html')


# Checkout page (processing order)
@login_required
def checkout_view(request):
    if request.method == 'POST':
        # Collect order details
        item_name = request.POST.get('item_name')
        item_id = request.POST.get('item_id')
        unit_price = float(request.POST.get('unit_price'))
        quantity = int(request.POST.get('quantity'))
        total_price = float(request.POST.get('total_price'))

        # Create an order object
        Order.objects.create(
            item_name=item_name,
            item_id=item_id,
            unit_price=unit_price,
            quantity=quantity,
            total_price=total_price
        )
        return redirect('order_success')  # Redirect to order success page after order is placed

    # If GET request, display the checkout page with pre-populated product details
    else:
        item_name = request.GET.get('name')
        item_id = request.GET.get('id')
        unit_price = request.GET.get('unit_price')
        return render(request, 'checkout.html', {
            'item_name': item_name,
            'item_id': item_id,
            'unit_price': unit_price
        })


# Send a message (contact form)
@login_required
def send_message(request):
    if request.method == 'POST':
        # Collect form data and save it as a new message in the database
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')

        Message.objects.create(
            name=name,
            email=email,
            message=message_text
        )

        return redirect('messages')  # Redirect to the messages page after sending a message

    return render(request, 'contact.html')


# View all messages (admin side)
@login_required
def view_messages(request):
    context = {
        'messages': Message.objects.all()
    }
    return render(request, 'viewmessages.html', context)


# Static about page
@login_required
def about(request):
    return render(request, 'about.html')


# Static contact page
@login_required
def contact(request):
    return render(request, 'contact.html')


# Search products functionality
@login_required
@require_POST
def search_products(request):
    query = request.POST.get('search', '').strip()
    products = Product.objects.filter(name__icontains=query)  # Search for products by name
    return render(request, 'products.html', {'products': products, 'query': query})


# List all products
@login_required
def products(request):
    context = {
        "products": Product.objects.all()  # Get all products from the database
    }
    return render(request, 'products.html', context)


# Home page
@login_required
def index(request):
    return render(request, 'index.html')


# Login page (for authentication)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('admin_index')  # Redirect to admin dashboard if user is a superuser
            login(request, user)
            return redirect('index')  # Redirect to home page for regular users
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


# Get product data as JSON
@login_required
def get_product_data(request, pk):
    product = Product.objects.get(pk=pk)
    data = {
        'id': product.pk,
        'name': product.name,
        'price': product.unit_price,
        'image': product.image.url,
        'seller': product.seller,
    }
    return JsonResponse(data)


# Delete a message
def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    message.delete()
    return redirect('messages')


"""
ADMIN VIEWS
"""

# Admin view for managing messages
@login_required(login_url='/login/admin/')
def admin_messages(request):
    context = {
        'messages': Message.objects.all()
    }
    return render(request, 'core/viewmessages.html', context)


# Mark message as read (via AJAX)
@login_required
def mark_as_read(request, pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            message = Message.objects.get(pk=pk)
            message.status = True
            message.save()
            return JsonResponse({'success': True})
        except Message.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Message not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


# Admin home page
@login_required
def admin_index(request):
    return render(request, 'core/index.html')


# Delete a product from the admin dashboard
@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return redirect('admin_products')


# Add a new product from the admin dashboard
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_index')
    else:
        form = ProductForm()

    return render(request, 'core/add_products.html', {'form': form})


# Admin view for managing products
@login_required
def admin_products(request):
    context = {
        "products": Product.objects.all()
    }
    return render(request, 'core/products.html', context)


# Admin view for managing orders
@login_required
def admin_orders(request):
    context = {
        'orders': Order.objects.all()
    }
    return render(request, 'core/orders.html', context)


# Admin view for success after completing an order
@login_required
def admin_order_success(request):
    return render(request, 'core/success.html')


# Complete an order from the admin dashboard
@login_required
def complete_order(request, pk):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)
        order.status = 1  # Mark order as complete
        order.save()
        return redirect('admin_orders')


# Update order details from the admin dashboard
@login_required
def update_order(request, pk):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)
        quantity = request.POST.get('quantity')
        total_price = request.POST.get('total_price')

        order.quantity = quantity
        order.total_price = total_price
        order.save()
        return redirect('orders')


# Update product details from the admin dashboard
@login_required
def update_product(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        name = request.POST.get('name')
        unit_price = request.POST.get('price')
        seller = request.POST.get('seller')
        product.name = name
        product.unit_price = unit_price
        product.seller = seller
        product.save()
        return redirect('admin_products')
    return redirect('admin_products')


# Admin-side search for products
@login_required
@require_POST
def admin_search_products(request):
    query = request.POST.get('search', '').strip()
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'core/products.html', {'products': products, 'query': query})


# Create superuser for the admin
def create_superuser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_superuser = True
            user.is_staff = True
            user.email = "email@gmail.com"
            user.save()
            messages.success(request, "Superuser created successfully!")
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'core/create_superuser.html', {'form': form})


# Update a message in the admin view
@login_required
def update_message(request, id):
    if request.method == 'POST':
        message = get_object_or_404(Message, pk=id)
        content = request.POST.get('message')
        message.message = content
        message.save()
        return redirect('messages')
    return redirect('messages')
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Product, Message, Order
from django.contrib import messages
from .forms import ProductForm
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login


# Logout the user and redirect to login page
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to your login page


# Register new users
def register_user(request):
    if request.method == 'POST':
        # Collect form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate the password and ensure it matches the confirmation
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register_user')

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register_user')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register_user')

        # Create the new user and save it to the database
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect('index')  # Redirect to the home page after registration

    return render(request, 'register.html')  # Return the registration page if the method is GET


# Display orders (only for logged-in users)
@login_required
def orders(request):
    context = {
        'orders': Order.objects.all()
    }
    return render(request, 'orders.html', context)


# Success page for orders
@login_required
def order_success(request):
    return render(request, 'success.html')


# Checkout page (processing order)
@login_required
def checkout_view(request):
    if request.method == 'POST':
        # Collect order details
        item_name = request.POST.get('item_name')
        item_id = request.POST.get('item_id')
        unit_price = float(request.POST.get('unit_price'))
        quantity = int(request.POST.get('quantity'))
        total_price = float(request.POST.get('total_price'))

        # Create an order object
        Order.objects.create(
            item_name=item_name,
            item_id=item_id,
            unit_price=unit_price,
            quantity=quantity,
            total_price=total_price
        )
        return redirect('order_success')  # Redirect to order success page after order is placed

    # If GET request, display the checkout page with pre-populated product details
    else:
        item_name = request.GET.get('name')
        item_id = request.GET.get('id')
        unit_price = request.GET.get('unit_price')
        return render(request, 'checkout.html', {
            'item_name': item_name,
            'item_id': item_id,
            'unit_price': unit_price
        })


# Send a message (contact form)
@login_required
def send_message(request):
    if request.method == 'POST':
        # Collect form data and save it as a new message in the database
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')

        Message.objects.create(
            name=name,
            email=email,
            message=message_text
        )

        return redirect('messages')  # Redirect to the messages page after sending a message

    return render(request, 'contact.html')


# View all messages (admin side)
@login_required
def view_messages(request):
    context = {
        'messages': Message.objects.all()
    }
    return render(request, 'viewmessages.html', context)


# Static about page
@login_required
def about(request):
    return render(request, 'about.html')


# Static contact page
@login_required
def contact(request):
    return render(request, 'contact.html')


# Search products functionality
@login_required
@require_POST
def search_products(request):
    query = request.POST.get('search', '').strip()
    products = Product.objects.filter(name__icontains=query)  # Search for products by name
    return render(request, 'products.html', {'products': products, 'query': query})


# List all products
@login_required
def products(request):
    context = {
        "products": Product.objects.all()  # Get all products from the database
    }
    return render(request, 'products.html', context)


# Home page
@login_required
def index(request):
    return render(request, 'index.html')


# Login page (for authentication)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('admin_index')  # Redirect to admin dashboard if user is a superuser
            login(request, user)
            return redirect('index')  # Redirect to home page for regular users
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


# Get product data as JSON
@login_required
def get_product_data(request, pk):
    product = Product.objects.get(pk=pk)
    data = {
        'id': product.pk,
        'name': product.name,
        'price': product.unit_price,
        'image': product.image.url,
        'seller': product.seller,
    }
    return JsonResponse(data)


# Delete a message
def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    message.delete()
    return redirect('messages')


"""
ADMIN VIEWS
"""

# Admin view for managing messages
@login_required(login_url='/login/admin/')
def admin_messages(request):
    context = {
        'messages': Message.objects.all()
    }
    return render(request, 'core/viewmessages.html', context)


# Mark message as read (via AJAX)
@login_required
def mark_as_read(request, pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            message = Message.objects.get(pk=pk)
            message.status = True
            message.save()
            return JsonResponse({'success': True})
        except Message.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Message not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


# Admin home page
@login_required
def admin_index(request):
    return render(request, 'core/index.html')


# Delete a product from the admin dashboard
@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return redirect('admin_products')


# Add a new product from the admin dashboard
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_index')
    else:
        form = ProductForm()

    return render(request, 'core/add_products.html', {'form': form})


# Admin view for managing products
@login_required
def admin_products(request):
    context = {
        "products": Product.objects.all()
    }
    return render(request, 'core/products.html', context)


# Admin view for managing orders
@login_required
def admin_orders(request):
    context = {
        'orders': Order.objects.all()
    }
    return render(request, 'core/orders.html', context)


# Admin view for success after completing an order
@login_required
def admin_order_success(request):
    return render(request, 'core/success.html')


# Complete an order from the admin dashboard
@login_required
def complete_order(request, pk):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)
        order.status = 1  # Mark order as complete
        order.save()
        return redirect('admin_orders')


# Update order details from the admin dashboard
@login_required
def update_order(request, pk):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)
        quantity = request.POST.get('quantity')
        total_price = request.POST.get('total_price')

        order.quantity = quantity
        order.total_price = total_price
        order.save()
        return redirect('orders')


# Update product details from the admin dashboard
@login_required
def update_product(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        name = request.POST.get('name')
        unit_price = request.POST.get('price')
        seller = request.POST.get('seller')
        product.name = name
        product.unit_price = unit_price
        product.seller = seller
        product.save()
        return redirect('admin_products')
    return redirect('admin_products')


# Admin-side search for products
@login_required
@require_POST
def admin_search_products(request):
    query = request.POST.get('search', '').strip()
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'core/products.html', {'products': products, 'query': query})


# Create superuser for the admin
def create_superuser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_superuser = True
            user.is_staff = True
            user.email = "email@gmail.com"
            user.save()
            messages.success(request, "Superuser created successfully!")
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'core/create_superuser.html', {'form': form})


# Update a message in the admin view
@login_required
def update_message(request, id):
    if request.method == 'POST':
        message = get_object_or_404(Message, pk=id)
        content = request.POST.get('message')
        message.message = content
        message.save()
        return redirect('messages')
    return redirect('messages')
