from rest_framework import serializers
from products.models import Products
from textilebale.models import TextileBale
from order.models import Order
from footagent.models import FootAgent 
from footagent.models import AgentAssignment


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

        
class TextileBaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextileBale
        fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class FootAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootAgent
        fields = '__all__'

class AgentAssignmentSerializer(serializers.ModelSerializer):
    foot_agent = FootAgentSerializer(read_only=True)
    
    class Meta:
        model = AgentAssignment
        fields = '__all__'
