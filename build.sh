#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Load initial product data
python manage.py shell -c "
from shop.models import Product
if Product.objects.count() == 0:
    Product.objects.create(title='Shirt', brand='Allen Solly', description='Light blue formal shirt for men.', price=599.0, category='men', image='products/shirt.png')
    Product.objects.create(title='Pant', brand='Peter England', description='Dark navy formal pants for men.', price=799.0, category='men', image='products/pant.png')
    Product.objects.create(title='T-Shirt', brand='US Polo', description='Comfortable navy blue t-shirt.', price=500.0, category='men', image='products/tshirt.png')
    Product.objects.create(title='Casual Jacket', brand='Levis', description='A stylish casual jacket for men.', price=1299.0, category='men', image='products/jacket.png')
    Product.objects.create(title='Designer Kurti', brand='Biba', description='Beautiful designer kurti for women.', price=899.0, category='women', image='products/kurti.png')
    print('Products loaded!')
else:
    print('Products already exist.')
"

# Create superuser if not exists
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@fashionhub.com', 'RAMADMIN2026')
    print('Admin user created!')
else:
    print('Admin already exists.')
"
