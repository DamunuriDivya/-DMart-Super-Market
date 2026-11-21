from django.db import models
from django.contrib.auth.models import User


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username + " - " + self.product_name
    from django.db import models
from django.contrib.auth.models import User


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username + " - " + self.product_name


class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    order_id = models.CharField(max_length=100, unique=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(max_length=100)

    order_status = models.CharField(
        max_length=50,
        default='Confirmed'
    )

    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

# Create your models here.
