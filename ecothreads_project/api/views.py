from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Products
from .serializers import ProductsSerializer, UserSerializer, TextileBaleSerializer
from order.models import Order
from .serializers import OrderSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
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
        return Response(serializer.data)

    def post(self, request):
        """
        Creates a new product.
        """
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductsDetailView(APIView):
    """
    API view for retrieving, updating and deleting products.
    """
    def get(self, request, pk):
        """
        Returns a product by id.
        """
        try:
            product = Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductsSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Updates a product by id.
        """
        try:
            product = Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductsSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Deletes a product by id.
        """
        try:
            product = Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Order Views
class OrderListCreateAPIView(APIView):
    """
    API view for listing and creating orders.
    """
    def get(self, request):
        """
        Returns a list of all orders.
        """
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Creates a new order.
        """
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    """
    API view for retrieving, updating and deleting a specific order.
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
        return Response(serializer.data)

    def put(self, request, order_id):
        """
        Updates a specific order by id.
        """
        order = self.get_object(order_id)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        """
        Deletes a specific order by id.
        """
        order = self.get_object(order_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

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

            # Notify the recycling company (optional)
            # Implement notification logic if needed

            return Response({"message": "Order placed successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Creates a new textile bale.
        """
        serializer = TextileBaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TextileBaleDetailAPIView(APIView):
    """
    API view for retrieving, updating and deleting a specific textile bale.
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
        return Response(serializer.data)

    def put(self, request, bale_id):
        """
        Updates a specific textile bale by id.
        """
        bale = self.get_object(bale_id)
        serializer = TextileBaleSerializer(bale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, bale_id):
        """
        Deletes a specific textile bale by id.
        """
        bale = self.get_object(bale_id)
        bale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
