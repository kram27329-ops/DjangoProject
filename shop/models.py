from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# ---------------- PRODUCT ----------------
class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    category = models.CharField(max_length=50)

    # CLOUDINARY IMAGE (IMPORTANT FIX)
    image = CloudinaryField('image')

    def __str__(self):
        return self.title


# ---------------- CART ----------------
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"