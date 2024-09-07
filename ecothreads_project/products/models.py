from django.db import models
from traders.models import Trader

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    material = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
