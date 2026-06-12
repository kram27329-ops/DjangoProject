from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('product/<int:id>/', views.product_detail, name='product_detail'),

    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),

    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart-increase/<int:id>/', views.cart_increase, name='cart_increase'),
    path('cart-decrease/<int:id>/', views.cart_decrease, name='cart_decrease'),
    path('cart-remove/<int:id>/', views.cart_remove, name='cart_remove'),

   path('men/', views.men_products, name='men_products'),
   path('women/', views.women_products, name='women_products'),
   path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard')
]