from rest_framework import serializers
from products.models import Products
from users.models import User
from order.models import Order
from textilebale.models import TextileBale
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