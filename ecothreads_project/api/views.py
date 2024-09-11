from django.http import JsonResponse, Http404
from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count

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

        status_data = Order.objects.filter(date__range=[start_date, end_date]).values('status').annotate(total_orders=Count('id'))
        return list(status_data)
