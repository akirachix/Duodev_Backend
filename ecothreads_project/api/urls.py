from django.urls import path
from .views import ProductsListView, ProductsDetailView
from .views import UserRegistrationView

urlpatterns = [
    path('products/', ProductsListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductsDetailView.as_view(), name='product_detail'),
    path('register/', UserRegistrationView.as_view(), name='register')
]

