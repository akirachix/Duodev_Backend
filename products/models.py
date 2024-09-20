from django.db import models
from traders.models import Trader

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    material = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)  
    trader = models.ForeignKey('traders.Trader', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.product_name
