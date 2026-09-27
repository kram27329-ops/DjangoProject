from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.conf import settings
from django.contrib import messages

from .models import Product, Cart, Order, OrderItem
from .forms import ProductForm


# ================= HOME =================
def home(request):
    products = Product.objects.all()

    form = None
    if request.user.is_authenticated and request.user.is_superuser:
        form = ProductForm()

    return render(request, 'home.html', {
        'products': products,
        'form': form,
    })


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
            return render(request, 'signup.html', {'error': 'User already exists'})

        user = User.objects.create_user(username=username, password=password)
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

        user = authenticate(request, username=username, password=password)

        if user:

            if role == "admin":
                if not user.is_superuser:
                    return render(request, 'login.html', {
                        'error': 'You are not Admin'
                    })

                if admin_code != settings.ADMIN_SECRET_CODE:
                    return render(request, 'login.html', {
                        'error': 'Invalid Admin Code'
                    })

                login(request, user)

                # Redirect to 'next' if provided, otherwise home
                next_url = request.GET.get('next') or request.POST.get('next', '')
                return redirect(next_url if next_url else 'home')

            # Normal user login
            login(request, user)

            # Redirect to 'next' if provided, otherwise home
            next_url = request.GET.get('next') or request.POST.get('next', '')
            return redirect(next_url if next_url else 'home')

        return render(request, 'login.html', {
            'error': 'Invalid credentials'
        })

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

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('home')

    return redirect('home')

# ================= EDIT PRODUCT =================
@login_required
def edit_product(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Admin only")

    product = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if form.is_valid():
        form.save()
        messages.success(request, 'Product updated!')
        return redirect('home')

    return render(request, 'add_product.html', {'form': form})


# ================= DELETE PRODUCT =================
@login_required
def delete_product(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Admin only")

    product = get_object_or_404(Product, id=id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect('home')


# ================= ADD TO CART =================
@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'"{product.title}" added to your cart!')
    return redirect('cart')


# ================= CART PAGE =================
@login_required
def cart(request):
    items = Cart.objects.filter(user=request.user).select_related('product')
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
    messages.success(request, f'"{item.product.title}" removed from cart.')
    return redirect('cart')


# ================= CHECKOUT =================
@login_required
def checkout(request):
    items = Cart.objects.filter(user=request.user).select_related('product')

    if not items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')

    total = sum(item.product.price * item.quantity for item in items)

    if request.method == "POST":
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        pincode = request.POST.get('pincode', '').strip()

        if not all([full_name, phone, address, city, pincode]):
            return render(request, 'checkout.html', {
                'items': items,
                'total': total,
                'error': 'Please fill all fields!'
            })

        # Create the order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address,
            city=city,
            pincode=pincode,
            total=total
        )

        # Create order items from cart
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear the cart
        items.delete()

        messages.success(request, 'Order placed successfully!')
        return redirect('order_success', order_id=order.id)

    return render(request, 'checkout.html', {
        'items': items,
        'total': total
    })


# ================= ORDER SUCCESS =================
@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.select_related('product')

    return render(request, 'order_success.html', {
        'order': order,
        'order_items': order_items
    })


# ================= MY ORDERS =================
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})


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
    orders = Order.objects.all().order_by('-created_at')

    return render(request, 'admin_dashboard.html', {
        'products': products,
        'users': users,
        'orders': orders
    })