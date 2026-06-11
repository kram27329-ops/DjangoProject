from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart
from .forms import ProductForm


def home(request):
    return render(request, 'home.html')
    products = Product.objects.all()

    if search:
        products = products.filter(title__icontains=search)

    # cart count (optional but useful)
    cart_count = Cart.objects.count()

    return render(request, 'home.html', {
        'products': products,
        'cart_count': cart_count
    })


# 👔 MEN PRODUCTS
def men_products(request):
    products = Product.objects.filter(category__iexact='men')
    return render(request, 'products.html', {'products': products})


# 👗 WOMEN PRODUCTS
def women_products(request):
    products = Product.objects.filter(category__iexact='women')
    return render(request, 'products.html', {'products': products})


# ➕ ADD PRODUCT (admin side)
def add_product(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'add_product.html', {'form': form})


# 🔍 PRODUCT DETAIL PAGE
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_details.html', {'product': product})


# 🛒 ADD TO CART
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    Cart.objects.create(product=product)

    return redirect('/cart/')


# 🛒 CART PAGE
def cart(request):
    cart_items = Cart.objects.all()

    return render(request, 'cart.html', {
        'cart_items': cart_items
    })