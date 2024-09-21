from django.http import JsonResponse, Http404
from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from products.models import Products
from .serializers import ProductsSerializer,ReviewSerializer
from rest_framework import generics
from textilebale.models import TextileBale
from .serializers import TextileBaleSerializer
from order.models import Order
from .serializers import OrderSerializer
from footagent.models import FootAgent, AgentAssignment
from .serializers import FootAgentSerializer, AgentAssignmentSerializer
from company.models import Company
from .serializers import CompanySignUpSerializer, CompanySignInSerializer
from .email_utils import send_invite_email
from rest_framework.decorators import api_view
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, EmailMultiAlternatives
from reviews.models import Review
from traders.models import Trader
from django.db.models.functions import TruncMonth
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator




from .serializers import (
    ProductsSerializer, UserSerializer, TextileBaleSerializer,
    SalesReportSerializer, ProductSalesReportSerializer,
    OrderStatusReportSerializer, CustomerActivityReportSerializer,
    OrderSerializer
)
import json
from products.models import Products
from order.models import Order
from django.contrib.auth.models import User
from textilebale.models import TextileBale
from datetime import timedelta
from django.utils import timezone


# Products Views
class ProductsListView(APIView):
    """
    API view for listing and creating products.
    """
    def get(self, request):
        """
        Returns a list of all products.
        """
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many=True)
        return JsonResponse({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Creates a new product.
        """
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


#ProductsdetailView
class ProductsDetailView(APIView):
    """
    API view for retrieving, updating, and deleting products.
    """
    def get(self, request, pk):
        """
        Returns a product by id.
        """
        try:
            product = Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return JsonResponse({'errors': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductsSerializer(product)
        return JsonResponse({'data': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Updates a product by id.
        """
        try:
            product = Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return JsonResponse({'errors': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductsSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'data': serializer.data}, status=status.HTTP_200_OK)
        return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Deletes a product by id.
        """
        try:
            product = Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return JsonResponse({'errors': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# User Registration View
class UserRegistrationView(APIView):
    """
    API view for creating a new user.
    """
    def post(self, request):
        """
        Creates a new user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
# Order Views
class OrderListCreateAPIView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailAPIView(APIView):
    """
    API view for retrieving, updating, and deleting a specific order.
    """
    def get_object(self, id):
        try:
            return Order.objects.get(id=id)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, id):
        """
        Returns a specific order by id.
        """
        order = self.get_object(id)
        serializer = OrderSerializer(order)
        return JsonResponse({'data': serializer.data}, status=status.HTTP_200_OK)

    
    def put(self, request, id):
        """
        Updates a specific order by id.
        """
        order = self.get_object(id)
        serializer = OrderSerializer(order, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """
        Deletes a specific order by id.
        """
        order = self.get_object(id)
        order.delete()
        return JsonResponse({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
class CartCheckoutAPIView(APIView):
    """
    API view to checkout and create an order from the cart.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Creates an order from the cart data.
        """
        cart_data = request.data.get('cart', [])
        user = request.user  # Assuming user is authenticated

        if not cart_data:
            return JsonResponse({'errors': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        order_data = {
            'user': user.id,
            'status': 'Pending',
            'total_price': sum(item['price'] * item['quantity'] for item in cart_data),
        }

        serializer = OrderSerializer(data=order_data)
        if serializer.is_valid():
            order = serializer.save()

            # Process cart items
            for item in cart_data:
                # Create OrderItem or similar model here
                pass

            return JsonResponse({'message': 'Order placed successfully', 'order_id': order.id}, status=status.HTTP_201_CREATED)

        return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Textile Bale Views
class TextileBaleListView(APIView):
    """
    API view for listing and creating textile bales.
    """
    def get(self, request):
        """
        Returns a list of all textile bales.
        """
        bales = TextileBale.objects.all()
        serializer = TextileBaleSerializer(bales, many=True)
        return JsonResponse({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Creates a new textile bale.
        """
        serializer = TextileBaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class TextileBaleDetailAPIView(APIView):
    """
    API view for retrieving, updating, and deleting a specific textile bale.
    """
    def get_object(self, bale_id):
        try:
            return TextileBale.objects.get(id=bale_id)
        except TextileBale.DoesNotExist:
            raise Http404

    def get(self, request, bale_id):
        """
        Returns a specific textile bale by id.
        """
        bale = self.get_object(bale_id)
        serializer = TextileBaleSerializer(bale)
        return JsonResponse({'data': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, bale_id):
        """
        Updates a specific textile bale by id.
        """
        bale = self.get_object(bale_id)
        serializer = TextileBaleSerializer(bale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'data': serializer.data}, status=status.HTTP_200_OK)
        return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, bale_id):
        """
        Deletes a specific textile bale by id.
        """
        bale = self.get_object(bale_id)
        bale.delete()
        return JsonResponse({'message': 'Textile bale deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# Sales Report Views
class TopSoldProductOfWeekAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Calculate the start of the week
        start_of_week = timezone.now() - timedelta(days=7)

        # Query to get the top sold product of the week
        top_sold_product = Order.objects.filter(
            order_date__gte=start_of_week
        ).values('product').annotate(
            total_quantity=Count('quantity')
        ).order_by('-total_quantity').first()

        if top_sold_product:
            # Fetch the product details
            product = Products.objects.get(pk=top_sold_product['product'])
            return Response({
                'product': ProductsSerializer(product).data,
                'total_sales': top_sold_product['total_quantity']
            })
        
        return Response({'error': 'No data available'}, status=status.HTTP_404_NOT_FOUND)


#TRADERS INTERACTIONS
class TradersInteractedAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Query to get the number of interactions per foot agent
        interactions = AgentAssignment.objects.values('foot_agent').annotate(
            interaction_count=Count('assignment_id')
        ).order_by('-interaction_count')

        
        detailed_interactions = []
        for interaction in interactions:
            foot_agent = FootAgent.objects.get(pk=interaction['foot_agent'])
            detailed_interactions.append({
                'agent_name': foot_agent.agent_name,
                'interaction_count': interaction['interaction_count'],
            })

        return Response(detailed_interactions)



#Registered Traders

User = get_user_model()
class SellersAPIView(APIView):
    def get(self, request):
        sellers = User.objects.filter(role='seller')  # Fetch sellers
        return Response({'sellers': [str(seller) for seller in sellers]})

#Totalsales
class TotalSalesAPIView(APIView):
    def get(self, request):
        # Group orders by month and sum total_price for each month
        sales_by_month = (
            Order.objects.annotate(month=TruncMonth('order_date'))
            .values('month')
            .annotate(total_sales=Sum('total_price'))
            .order_by('month')
        )

        # Prepare the data with full month names
        monthly_sales = [
            {'month': sale['month'].strftime('%B %Y'), 'total_sales': sale['total_sales']}
            for sale in sales_by_month
        ]

        # Return the result as a JSON response
        return JsonResponse({'monthly_sales': monthly_sales})


# Textile Bale:
class TextileBaleListCreateView(generics.ListCreateAPIView):
    queryset = TextileBale.objects.all()
    serializer_class = TextileBaleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # Add filtering logic (e.g., by waste_type, location) if needed
        waste_type = self.request.query_params.get('waste_type', None)
        location = self.request.query_params.get('location', None)
        
        if waste_type:
            queryset = queryset.filter(waste_type=waste_type)
        if location:
            queryset = queryset.filter(location=location)
        
        return queryset



# Retrieve, update, or delete a specific bale
class TextileBaleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TextileBale.objects.all()
    serializer_class = TextileBaleSerializer
    lookup_field = 'bale_id'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Textile bale deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



# Order table
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset



# Retrieve, update, or delete a specific order
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'order_id'




# Checkout and create an order from the cart 
class CartCheckoutView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        # Assuming `cart_data` comes from the request 
        cart_data = self.request.data.get('cart', {})
        # Calculate total_price, create an order, etc.
        total_price = sum(item['price'] * item['quantity'] for item in cart_data)
        serializer.save(total_price=total_price)



# footagent and assignment
class FootAgentCreateView(APIView):
    def post(self, request):
        serializer = FootAgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class FootAgentListCreateView(generics.ListCreateAPIView):
    queryset = FootAgent.objects.all()
    serializer_class = FootAgentSerializer

class FootAgentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FootAgent.objects.all()
    serializer_class = FootAgentSerializer



# Assignment views
class AgentAssignmentListCreateView(generics.ListCreateAPIView):
    queryset = AgentAssignment.objects.all()
    serializer_class = AgentAssignmentSerializer

class AgentAssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AgentAssignment.objects.all()
    serializer_class = AgentAssignmentSerializer





# company signup and signin
class CompanySignUpView(APIView):
    def post(self, request):
        serializer = CompanySignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Company registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanySignInView(APIView):
    def post(self, request):
        serializer = CompanySignInSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Company signed in successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# sending  invitation emails

def send_invite_email(recipient, subject, html_content, text_content):
    """
    Utility function to send an email invitation.
    """
    email = EmailMultiAlternatives(subject, text_content, 'ecothreadshub2024@gmail.com', [recipient])
    email.attach_alternative(html_content, "text/html")
    email.send()

@api_view(['POST'])
def send_invitation_email(request):
    """
    API endpoint to send an invitation email to a worker.
    """
    subject = "Welcome to Eco Threads Hub!"
    message = "You have been invited to join Eco Threads Hub as a foot agent. We hope to see you soon!"
    recipient = request.data.get('recipient')
    registration_link = "#"  # link to our website to register

    if not subject or not message or not recipient:
        return Response({'error': 'Subject, message, and recipient email are required.'}, status=400)

    # Validate email format
    try:
        validate_email(recipient)
    except ValidationError:
        return Response({'error': 'Invalid email address format.'}, status=400)

    # Prepare the HTML content with the template
    html_content = f"""
        <html>
        <head>
            <style>
                .container {{
                    width: 80%;
                    margin: 0 auto;
                    padding: 20px;
                    font-family: Arial, sans-serif;
                }}
                .header {{
                    text-align: center;
                    background-color: #f7f7f7;
                    padding: 20px;
                }}
                .logo {{
                    width: 150px;
                }}
                .button {{
                    display: inline-block;
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    font-size: 16px;
                    border-radius: 5px;
                }}
                .footer {{
                    margin-top: 20px;
                    text-align: center;
                    font-size: 12px;
                    color: #777;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <img class="logo" src="https://lh3.googleusercontent.com/a/ACg8ocJngyBoQ9rtDOs1iY84zWb43oA_cX6qzgbDiXQMy5kU4rkYa5E=s96-c-rg-br100" alt="Eco Threads Hub Logo">
                    <h1>Welcome to Eco Threads Hub!</h1>
                </div>
                <p>Hello,</p>
                <p>You have been invited to join Eco Threads Hub as a foot agent. We are excited to have you as part of our growing team and look forward to your contributions to sustainability and textile recycling efforts.</p>
                <p>To get started, please click the button below to complete your registration:</p>
                <a href="{{registration_link}}" class="button">Complete Registration</a>
                <p>If you have any questions, feel free to reach out to us.</p>
                <p>Best regards,<br>The Eco Threads Team</p>
                <div class="footer">
                    <p>If you did not expect this invitation, please disregard this email.</p>
                </div>
            </div>
        </body>
        </html>
        """

    # Send the email using the utility function
    try:
        send_invite_email(recipient, subject, html_content, message)
        return Response({'success': f'Email sent to {recipient}.'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

        status_data = Order.objects.filter(date__range=[start_date, end_date]).values('status').annotate(total_orders=Count('id'))
        return list(status_data)
# Review views
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    
    
    

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(View):
    """Handle user login."""

    from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate
import json

def post(self, request, *args, **kwargs):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required.'}, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Serialize user data
            user_data = {
                'user_id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'last_login': user.last_login,
                # Add any other fields you want to include
            }
            return JsonResponse({'message': 'Login successful', 'user': user_data})
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)        
        
        
        