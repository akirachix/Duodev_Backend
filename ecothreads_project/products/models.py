from django.db import models

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    material = models.CharField(max_length=255)
    description = models.TextField()
    # trader_id = models.IntegerField()  # Assuming trader_id is a foreign key, replace this with a ForeignKey if you have a Trader model.

    def __str__(self):
        return self.product_name



