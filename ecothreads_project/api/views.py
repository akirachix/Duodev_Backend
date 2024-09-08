import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Products
from .serializers import ProductsSerializer
from rest_framework import generics
from textilebale.models import TextileBale
from .serializers import TextileBaleSerializer
from order.models import Order
from .serializers import OrderSerializer
from footagent.models import FootAgent, AgentAssignment
from .serializers import FootAgentSerializer, AgentAssignmentSerializer


<<<<<<<<<<<<<<  ✨ Codeium Command 🌟  >>>>>>>>>>>>>>>>
# API endpoint that allows products to be viewed or edited.
class ProductsListView(APIView):
<<<<<<<  af0e93a1-6fc0-41ae-8b2f-acf1dc7b2ea7  >>>>>>>
    def get(self, request):
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ProductsDetailView(APIView):
    def get(self, request, pk):
        try:
            product = Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductsSerializer(product)
        return Response(serializer.data)
    def put(self, request, pk):
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
        try:
            product = Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




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







