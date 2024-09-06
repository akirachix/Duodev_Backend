from django.urls import path
from .views import ProductsListView, ProductsDetailView

urlpatterns = [
    path('products/', ProductsListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductsDetailView.as_view(), name='product_detail'),
]

