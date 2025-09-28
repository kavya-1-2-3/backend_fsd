from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Product, Review
from .forms import CustomUserCreationForm, ReviewForm

# =========================
# AUTHENTICATION VIEWS
# =========================
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('product_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'website/common/signup.html', {'form': form})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('product_list')
        else:
            return render(request, 'website/common/login.html', {'error_message': 'Invalid username or password.'})
    return render(request, 'website/common/login.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    return redirect('login')

# =========================
# PRODUCT VIEWS
# =========================
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'website/common/product_list.html', {'products': products})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all().order_by('-created_at')
    form = ReviewForm()
    return render(request, 'website/common/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form
    })

@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
    return redirect('product_detail', pk=product.pk)

# =========================
# CART VIEWS
# =========================
@login_required
def add_to_cart(request, pk):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        cart[str(pk)] = cart.get(str(pk), 0) + quantity
        request.session['cart'] = cart
    return redirect('cart')

@login_required
def remove_from_cart(request, pk):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart.pop(str(pk), None)
        request.session['cart'] = cart
    return redirect('cart')

@login_required
def cart(request):
    cart = request.session.get('cart', {})
    cart_products = []
    subtotal = 0
    shipping = 50
    for pk_str, quantity in cart.items():
        product = get_object_or_404(Product, pk=int(pk_str))
        total_price = product.price * quantity
        subtotal += total_price
        cart_products.append({'product': product, 'quantity': quantity, 'total_price': total_price})
    order_total = subtotal + shipping
    return render(request, 'website/common/cart.html', {
        'cart_products': cart_products,
        'subtotal': subtotal,
        'shipping': shipping,
        'order_total': order_total
    })

@login_required
def checkout(request):
    # Clear the cart directly
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True

    # Redirect straight to order confirmation page
    return redirect('order_confirmation')


def order_confirmation(request):
    return render(request, 'website/common/order_confirmation.html')

@login_required
def search(request):
    """Temporary search page."""
    return render(request, 'website/common/product_list.html', {
        'products': Product.objects.all(),  # or [] if you want empty
        'title': 'Search Results'
    })
