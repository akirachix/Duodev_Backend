# reports/models.py

from django.db import models

class SalesReport(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    total_sales = models.DecimalField(max_digits=12, decimal_places=2)
    total_orders = models.IntegerField()
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sales Report from {self.start_date} to {self.end_date}"

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    order_number = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_placed = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.order_number

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    review_date = models.DateField()

    def __str__(self):
        return f"Review for {self.product.name} - Rating: {self.rating}"
