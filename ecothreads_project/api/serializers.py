from rest_framework import serializers
from products.models import Products
from textilebale.models import TextileBale
from order.models import Order
from footagent.models import FootAgent 
from footagent.models import AgentAssignment
from company.models import Company
from django.contrib.auth.hashers import make_password, check_password


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



# Company signing in

class CompanySignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Company
        fields = ['company_name', 'company_email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password field
        validated_data['password'] = make_password(validated_data['password'])  # Hash the password
        return super().create(validated_data)

class CompanySignInSerializer(serializers.Serializer):
    company_email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            company = Company.objects.get(company_email=data['company_email'])
        except Company.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")
        
        if not check_password(data['password'], company.password):
            raise serializers.ValidationError("Invalid email or password.")
        
        return data

