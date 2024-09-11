from django.http import JsonResponse, Http404
from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from products.models import Products
from .serializers import ProductsSerializer
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



from .serializers import (
    ProductsSerializer, UserSerializer, TextileBaleSerializer,
    SalesReportSerializer, ProductSalesReportSerializer,
    OrderStatusReportSerializer, CustomerActivityReportSerializer,
    OrderSerializer
)
from products.models import Products
from order.models import Order
from django.contrib.auth.models import User
from textilebale.models import TextileBale

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
            return JsonResponse({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


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
    def get_object(self, order_id):
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, order_id):
        """
        Returns a specific order by id.
        """
        order = self.get_object(order_id)
        serializer = OrderSerializer(order)
        return JsonResponse({'data': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, order_id):
        """
        Updates a specific order by id.
        """
        order = self.get_object(order_id)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'data': serializer.data}, status=status.HTTP_200_OK)
        return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        """
        Deletes a specific order by id.
        """
        order = self.get_object(order_id)
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
class TextileBaleListCreateAPIView(APIView):
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
class SalesReportAPIView(APIView):
    def get(self, request):
        serializer = SalesReportSerializer(data=request.query_params)
        if serializer.is_valid():
            data = self.generate_sales_report(serializer.validated_data)
            return JsonResponse(data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = SalesReportSerializer(data=request.data)
        if serializer.is_valid():
            data = self.generate_sales_report(serializer.validated_data)
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_sales_report(self, data):
        start_date = parse_date(data.get('start_date'))
        end_date = parse_date(data.get('end_date'))
        report_type = data.get('report_type')

        if not start_date or not end_date:
            return {'error': 'Start date and end date are required'}

        sales_data = Order.objects.filter(date__range=[start_date, end_date])

        if report_type == 'daily':
            report = sales_data.values('date').annotate(total_sales=Sum('total_price'))
        elif report_type == 'weekly':
            report = sales_data.extra({'week': "strftime('%Y-%W', date)"}).values('week').annotate(total_sales=Sum('total_price'))
        elif report_type == 'monthly':
            report = sales_data.extra({'month': "strftime('%Y-%m', date)"}).values('month').annotate(total_sales=Sum('total_price'))
        else:
            report = {'error': 'Invalid report type'}

        return list(report)


class ProductSalesReportAPIView(APIView):
    def get(self, request):
        serializer = ProductSalesReportSerializer(data=request.query_params)
        if serializer.is_valid():
            data = self.generate_product_sales_report(serializer.validated_data)
            return JsonResponse(data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_product_sales_report(self, data):
        start_date = parse_date(data.get('start_date'))
        end_date = parse_date(data.get('end_date'))

        if not start_date or not end_date:
            return {'error': 'Start date and end date are required'}

        sales_data = Order.objects.filter(date__range=[start_date, end_date]).values('product').annotate(total_sales=Sum('total_price'))
        return list(sales_data)


class CustomerActivityReportAPIView(APIView):
    def get(self, request):
        serializer = CustomerActivityReportSerializer(data=request.query_params)
        if serializer.is_valid():
            data = self.generate_customer_activity_report(serializer.validated_data)
            return JsonResponse(data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_customer_activity_report(self, data):
        start_date = parse_date(data.get('start_date'))
        end_date = parse_date(data.get('end_date'))

        if not start_date or not end_date:
            return {'error': 'Start date and end date are required'}

        activity_data = Order.objects.filter(date__range=[start_date, end_date]).values('user').annotate(total_orders=Count('id'))
        return list(activity_data)


class OrderStatusReportAPIView(APIView):
    def get(self, request):
        serializer = OrderStatusReportSerializer(data=request.query_params)
        if serializer.is_valid():
            data = self.generate_order_status_report(serializer.validated_data)
            return JsonResponse(data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_order_status_report(self, data):
        start_date = parse_date(data.get('start_date'))
        end_date = parse_date(data.get('end_date'))


        if not start_date or not end_date:
            return {'error': 'Start date and end date are required'}

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

# Checkout and create an order from the cart (mock implementation)
class CartCheckoutView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        # Assuming `cart_data` comes from the request (not implemented here)
        cart_data = self.request.data.get('cart', {})
        # Calculate total_price, create an order, etc.
        total_price = sum(item['price'] * item['quantity'] for item in cart_data)
        serializer.save(total_price=total_price)



# footagent and assignment

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
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ width: 100%; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #e2e2e2; border-radius: 10px; background-color: #f9f9f9; }}
            .header {{ text-align: center; margin-bottom: 20px; }}
            .footer {{ margin-top: 20px; font-size: 12px; color: #888; }}
            .button {{ display: inline-block; padding: 10px 15px; margin-top: 20px; background-color: #28a745; color: #ffffff; text-decoration: none; border-radius: 5px; }}
            .logo {{ max-width: 200px;height: auto;}}
            p {{ color: black; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="https://lh3.googleusercontent.com/a/ACg8ocJngyBoQ9rtDOs1iY84zWb43oA_cX6qzgbDiXQMy5kU4rkYa5E=s96-c-rg-br100" alt="Eco Threads Hub Logo" class="logo"/>
                <h2>Welcome to Eco Threads Hub! </h2>
            </div>
            <p>Dear {recipient},</p>
            <p>{message}</p>
            <p>We are excited to have you join us. Click the button below to register:</p>
            <a href="{registration_link}" class="button">Join Now</a>
            <p>Best regards,<br>Eco Threads Hub</p>
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
