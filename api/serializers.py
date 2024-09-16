from rest_framework import serializers
from products.models import Products
from users.models import User
from order.models import Order
from textilebale.models import TextileBale
from reports.models import SalesReport, Product, Order, Review
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

class OrderCreateView(serializers.ModelSerializer):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    
    
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


class CustomerActivityReportSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

        
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
        fields = ['agent_id', 'user', 'agent_name', 'location']
        extra_kwargs = {
            'user': {'required': True},
            'agent_name': {'required': True},
        }

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
    
#Serializer for Review
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        
        
#Serializer for Trader
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'phone_number', 'registration_date', 'role']
    
    def create(self, validated_data):
        # Use the create_user method to handle password hashing
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            registration_date=validated_data.get('registration_date', None),
            role=validated_data.get('role', 'public'),
        )        