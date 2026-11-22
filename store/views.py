from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .models import Wishlist, Order

import uuid


# Product Price Dictionary
PRODUCTS = {
    'Rice': 100,
    'Milk': 30,
    'Apples': 120,
    'Potatoes': 40,
    'Sugar': 45,
    'Cooking Oil': 150,
    'Wheat Flour': 55,
    'Toor Dal': 120,
    'Soap': 35,
    'Shampoo': 90,
    'Biscuits': 20,
    'Tea Powder': 80,
    'Coffee Powder': 110,
    'Bread': 40,
}


# Home Page
def home(request):
    return render(request, 'home.html')


# Products Page
# Products Page
def products(request):

    product_list = [
        {'name': 'Rice', 'price': 100, 'discount': 10, 'image': 'store/images/rice.jpg'},
        {'name': 'Milk', 'price': 30, 'discount': 5, 'image': 'store/images/milk.jpg'},
        {'name': 'Apples', 'price': 120, 'discount': 10, 'image': 'store/images/apples.jpg'},
        {'name': 'Potatoes', 'price': 40, 'discount': 10, 'image': 'store/images/potatoes.jpg'},
        {'name': 'Sugar', 'price': 45, 'discount': 10, 'image': 'store/images/sugar.jpg'},
        {'name': 'Cooking Oil', 'price': 150, 'discount': 15, 'image': 'store/images/oil.jpg'},
        {'name': 'Wheat Flour', 'price': 55, 'discount': 10, 'image': 'store/images/wheat.jpg'},
        {'name': 'Toor Dal', 'price': 120, 'discount': 5, 'image': 'store/images/toor_dal.jpg'},
        {'name': 'Soap', 'price': 35, 'discount': 10, 'image': 'store/images/soap.jpg'},
        {'name': 'Shampoo', 'price': 90, 'discount': 15, 'image': 'store/images/shampoo.jpg'},
        {'name': 'Biscuits', 'price': 20, 'discount': 5, 'image': 'store/images/biscuits.jpg'},
        {'name': 'Tea Powder', 'price': 80, 'discount': 10, 'image': 'store/images/tea.jpg'},
        {'name': 'Coffee Powder', 'price': 110, 'discount': 15, 'image': 'store/images/coffee.jpg'},
        {'name': 'Bread', 'price': 40, 'discount': 5, 'image': 'store/images/bread.jpg'},
    ]

    # Calculate Discount Price
    for product in product_list:

        original_price = product['price']
        discount = product['discount']

        offer_price = original_price - (original_price * discount / 100)

        product['original_price'] = original_price
        product['offer_price'] = round(offer_price, 2)

    # Search Functionality
    search_query = request.GET.get('search', '').strip().lower()

    if search_query:
        product_list = [
            product for product in product_list
            if search_query in product['name'].lower()
        ]

    return render(request, 'products.html', {
        'products': product_list,
        'search_query': search_query
    })
# Add to Cart
def add_to_cart(request, product_name):

    if product_name not in PRODUCTS:
        messages.error(request, 'Invalid product!')
        return redirect('products')

    cart_items = request.session.get('cart', [])

    cart_items.append(product_name)

    request.session['cart'] = cart_items

    return redirect('cart')


# Cart Page
def cart(request):

    cart_items = request.session.get('cart', [])

    cart_data = []
    total_price = 0

    discounts = {
        'Rice': 10,
        'Milk': 5,
        'Apples': 10,
        'Potatoes': 0,
        'Sugar': 10,
        'Cooking Oil': 15,
        'Wheat Flour': 0,
        'Toor Dal': 5,
        'Soap': 10,
        'Shampoo': 15,
        'Biscuits': 0,
        'Tea Powder': 10,
        'Coffee Powder': 15,
        'Bread': 5,
    }

    for item in cart_items:

        if item in PRODUCTS:

            original_price = PRODUCTS[item]
            discount = discounts.get(item, 0)

            offer_price = original_price - (
                original_price * discount / 100
            )

            offer_price = round(offer_price, 2)

            cart_data.append({
                'name': item,
                'price': offer_price,
                'original_price': original_price,
                'discount': discount,
                'offer_price': offer_price
            })

            total_price += offer_price

    return render(request, 'cart.html', {
        'cart_items': cart_data,
        'total_price': round(total_price, 2)
    })
# Remove Product from Cart
def remove_from_cart(request, product_name):

    cart_items = request.session.get('cart', [])

    if product_name in cart_items:
        cart_items.remove(product_name)

    request.session['cart'] = cart_items

    return redirect('cart')
def register_page(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:

            messages.error(request, 'Passwords do not match!')

        elif User.objects.filter(username=username).exists():

            messages.error(request, 'Username already exists!')

        else:

            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            messages.success(request, 'Registration successful!')

            return redirect('login')

    return render(request, 'register.html')


# Login Page
def login_page(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        else:

            messages.error(request, 'Invalid username or password!')

    return render(request, 'login.html')


# Add to Wishlist
@login_required
def add_to_wishlist(request):

    if request.method == 'POST':

        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_image = request.POST.get('product_image')

        Wishlist.objects.get_or_create(
            user=request.user,
            product_name=product_name,
            defaults={
                'product_price': product_price,
                'product_image': product_image
            }
        )

        messages.success(request, 'Product added to Wishlist!')

    return redirect('products')


# Wishlist Page
@login_required
def wishlist_page(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    )

    return render(request, 'wishlist.html', {
        'wishlist_items': wishlist_items
    })


# Remove Wishlist
@login_required
def remove_wishlist(request, id):

    Wishlist.objects.filter(
        id=id,
        user=request.user
    ).delete()

    messages.success(request, 'Product removed from Wishlist!')

    return redirect('wishlist')


# Payment Page
@login_required
def payment_page(request):

    return render(request, 'payment.html')


# Process Payment
@login_required
def process_payment(request):

    if request.method == 'POST':

        payment_method = request.POST.get('payment_method')

        if not payment_method:

            messages.error(request, 'Please select a payment method!')

            return redirect('payment')

        request.session['payment_method'] = payment_method

        return confirm_order(request)

    return redirect('payment')


# Confirm Order
@login_required
def confirm_order(request):

    if request.method == 'POST':

        payment_method = request.session.get('payment_method')

        cart_items = request.session.get('cart', [])

        if not payment_method:

            messages.error(request, 'Please select a payment method!')

            return redirect('payment')

        if not cart_items:

            messages.error(request, 'Your cart is empty!')

            return redirect('cart')

        total_price = 0

        for item in cart_items:

            if item not in PRODUCTS:

                messages.error(request, 'Invalid product in cart!')

                return redirect('cart')

            total_price += PRODUCTS[item]

        order = Order.objects.create(
            user=request.user,
            order_id=str(uuid.uuid4())[:8].upper(),
            total_price=total_price,
            payment_method=payment_method,
            order_status='Confirmed'
        )

        request.session['cart'] = []

        request.session.pop('payment_method', None)

        return render(request, 'order_success.html', {
            'order': order
        })

    return redirect('payment')
# My Profile Page
@login_required
def profile_page(request):

    return render(request, 'profile.html', {
        'user': request.user
    })
def logout_page(request):
    logout(request)
    return redirect('home')
LOGIN_URL = '/login/'