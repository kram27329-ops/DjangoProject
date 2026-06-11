from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]

    # ➕ Add product
    path('add/', views.add_product, name='add_product'),

    # 👔 Men products
    path('men/', views.men_products, name='men_products'),

    # 👗 Women products
    path('women/', views.women_products, name='women_products'),

    # 🔍 Product detail page
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    # 🛒 Add to cart
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),

    # 🛒 Cart page
    path('cart/', views.cart, name='cart'),
]