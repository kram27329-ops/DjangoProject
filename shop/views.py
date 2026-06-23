from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.conf import settings


from .models import Product, Cart
from .forms import ProductForm

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

# ================= PRODUCT DETAIL =================
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_details.html', {'product': product})

# ================= SIGNUP =================
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'signup.html',
                {'error': 'User already exists'}
            )

        user = User.objects.create_user(
            username=username,
            password=password
        )

        user.is_superuser = False
        user.is_staff = False
        user.save()

        login(request, user)
        return redirect('home')

    return render(request, 'signup.html')
# ================= LOGIN =================
def login_view(request):

    if request.method == "POST":

        role = request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin_code = request.POST.get('admin_code', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            # Admin option select pannirundha
            if role == "admin":

                if not user.is_superuser:
                    return render(
                        request,
                        'login.html',
                        {'error': 'You are not an Admin'}
                    )

                if admin_code != settings.ADMIN_SECRET_CODE:
                    return render(
                        request,
                        'login.html',
                        {'error': 'Invalid Admin Secret Code'}
                    )

            login(request, user)
            return redirect('home')

        return render(
            request,
            'login.html',
            {'error': 'Invalid Username or Password'}
        )

    return render(request, 'login.html')


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('login')


# ================= ADD PRODUCT (ADMIN ONLY) =================
@login_required
def add_product(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Admin only")

    form = ProductForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('home')

    return render(request, 'add_product.html', {'form': form})


# ================= EDIT PRODUCT =================
@login_required
def edit_product(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Admin only")

    product = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if form.is_valid():
        form.save()
        return redirect('home')

    return render(request, 'add_product.html', {'form': form})


# ================= DELETE PRODUCT =================
@login_required
def delete_product(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Admin only")

    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('home')


# ================= ADD TO CART =================
@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()
    return redirect('cart')


# ================= CART PAGE =================
@login_required
def cart(request):
    items = Cart.objects.filter(user=request.user)

    total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })


# ================= CART INCREASE =================
@login_required
def cart_increase(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart')


# ================= CART DECREASE =================
@login_required
def cart_decrease(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


# ================= CART REMOVE =================
@login_required
def cart_remove(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    item.delete()
    return redirect('cart')


# ================= MEN PRODUCTS =================
def men_products(request):
    products = Product.objects.filter(category='men')
    return render(request, 'home.html', {'products': products})


# ================= WOMEN PRODUCTS =================
def women_products(request):
    products = Product.objects.filter(category='women')
    return render(request, 'home.html', {'products': products})


# ================= ADMIN DASHBOARD =================
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Admin only")

    products = Product.objects.all()
    users = User.objects.all()

    return render(request, 'admin_dashboard.html', {
        'products': products,
        'users': users
    })