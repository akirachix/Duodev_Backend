from django.db import models

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()  
    product_id = models.IntegerField()  
    order_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')  

    def __str__(self):
        return f"Order {self.order_id} by User {self.user_id}"
