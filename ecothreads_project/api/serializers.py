from rest_framework import serializers
from products.models import Products
from users.models import User
from order.models import Order
from textilebale.models import TextileBale
from reports.models import SalesReport, Product, Order, Review
#Serializer for Products
class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
#Serializer for User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

#Serializer for Order       


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
#Serializer for TextileBale

class TextileBaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextileBale
        fields = '__all__'
#Serializer for Sales report
class SalesReportSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    report_type = serializers.ChoiceField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')])

#Serializer for Product report
class ProductSalesReportSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    category = serializers.CharField(required=False)
    stock = serializers.IntegerField(required=False)
    popularity = serializers.CharField(required=False)

#Serializer for Order report
class OrderStatusReportSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    status = serializers.ChoiceField(choices=[('completed', 'Completed'), ('pending', 'Pending'), ('cancelled', 'Cancelled')])

#Serializer for Review report
class CustomerActivityReportSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
