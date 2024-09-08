from django.db import models

# Create your models here.

class Sales(models.Model):
    """
    Sales model to store the total amount of sales for a given date.
    """
    date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"Sales on {self.date} - ${self.total_amount}"

class Product(models.Model):
    """
    Product model to store the product name, category, stock, and price.
    """
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.name

class Order(models.Model):
    """
    Order model to store the order number, status, total amount, and date placed.
    """
    order_number = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_placed = models.DateField()


    def __str__(self):
        return self.order_number

class Review(models.Model):
    """
    Review model to store the product, rating, comment, and review date.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()# Example: Generate order report based on provided data
    comment = models.TextField()
    review_date = models.DateField()

    def __str__(self):
        return f"Review for {self.product.name} - Rating: {self.rating}"

