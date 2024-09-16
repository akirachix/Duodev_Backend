from django.contrib import admin
from .models import SalesReport, Product, Order, Review
from reports.models import SalesReport, Product, Order, Review
@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'total_sales', 'total_orders', 'generated_at')
    search_fields = ('start_date', 'end_date')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'stock', 'price')
    search_fields = ('name', 'category')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'status', 'total_price', 'date_placed')
    search_fields = ('order_number', 'status')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'rating', 'review_date')
    search_fields = ('product__name', 'rating')
