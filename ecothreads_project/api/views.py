"""
API views for products and user registration.

ProductsListView:
    - GET: Returns a list of all products.
    - POST: Creates a new product.

ProductsDetailView:
    - GET: Returns a product by id.
    - PUT: Updates a product by id.
    - DELETE: Deletes a product by id.

UserRegistrationView:
    - POST: Creates a new user.
"""
import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Products
from .serializers import ProductsSerializer
from .serializers import UserSerializer



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

