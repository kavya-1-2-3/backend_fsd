from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
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
        if user is not None:
            auth_login(request, user)
            return redirect('product_list')
        else:
            context = {'error_message': 'Invalid username or password.'}
            return render(request, "website/login.html", context) 
    return render(request, "website/common/login.html")

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')
def search(request):
    """Placeholder for a search functionality."""
    return render(request, "website/index.html", {
        'products': [],
        'title': 'Search Products',
        'description': 'Search for products here.'
    })

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'website/common/product_list.html', {'products': products})

from django.shortcuts import redirect

def home_redirect(request):
    """Redirect root URL to login or product list."""
    if request.user.is_authenticated:
        return redirect('product_list')
    else:
        return redirect('login')

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all().order_by('-created_at')
    form = ReviewForm()
    context = {
        'product': product,
        'reviews': reviews,
        'form': form
    }
    return render(request, 'website/common/product_detail.html', context)


@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user   # associate review with logged-in user
            review.save()
            return redirect('product_detail', pk=product.pk)
    return redirect('product_detail', pk=product.pk)


# =========================
# CART VIEWS
# =========================
@login_required
def add_to_cart(request, pk):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        pk_str = str(pk)
        cart[pk_str] = cart.get(pk_str, 0) + quantity
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart')



@login_required
def remove_from_cart(request, pk):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        pk_int = int(pk)
        cart = [item for item in cart if item != pk_int]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart')


@login_required
@login_required
def cart(request):
    cart = request.session.get('cart', {})
    cart_products = []
    subtotal = 0
    shipping = 50  # fixed shipping cost

    # Fetch products from DB and calculate totals
    for pk_str, quantity in cart.items():
        product = get_object_or_404(Product, pk=int(pk_str))
        total_price = product.price * quantity
        subtotal += total_price
        cart_products.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price
        })

    order_total = subtotal + shipping

    context = {
        'cart_products': cart_products,
        'subtotal': subtotal,
        'shipping': shipping,
        'order_total': order_total,
    }
    return render(request, 'website/common/cart.html', context)




@login_required
def checkout(request):
    if request.method == 'POST':
        if 'cart' in request.session:
            del request.session['cart']
        return redirect('order_confirmation')
    return redirect('cart')


def order_confirmation(request):
    return render(request, 'website/common/order_confirmation.html')


# =========================
# PRODUCT API VIEWS
# =========================
@csrf_exempt
def product_add(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product = Product.objects.create(
                name=data.get("name"), 
                description=data.get("description"),
                price=data.get("price"), 
                stock=data.get("stock")
            )
            return JsonResponse({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "stock": product.stock
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return HttpResponseBadRequest("Invalid request method")

def product_list(request):
    """Displays all products."""
    products = Product.objects.all()
    return render(request, 'website/common/product_list.html', {'products': products})
@csrf_exempt
def product_update(request, id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            product = Product.objects.get(pk=id)
            product.name = data.get("name", product.name)
            product.description = data.get("description", product.description)
            product.price = data.get("price", product.price)
            product.stock = data.get("stock", product.stock)
            product.save()
            return JsonResponse({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "stock": product.stock
            })
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return HttpResponseBadRequest("Invalid request method")
