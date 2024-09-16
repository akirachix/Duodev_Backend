from django.db import models
from products.models import Products
from users.models import User


class Order(models.Model):
    order_number = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Order {self.id} by User {self.user_id} in location {self.location}, phone: {self.phone_number}"
