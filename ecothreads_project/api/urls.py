from django.urls import path
from .views import (
    ProductsListView, ProductsDetailView, UserRegistrationView,
    OrderListCreateAPIView, OrderDetailAPIView, CartCheckoutAPIView,
    TextileBaleListCreateAPIView, TextileBaleDetailAPIView,
    SalesReportAPIView, ProductSalesReportAPIView, CustomerActivityReportAPIView,
    OrderStatusReportAPIView
)

urlpatterns = [
    path('products/', ProductsListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductsDetailView.as_view(), name='product-detail'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:order_id>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('checkout/', CartCheckoutAPIView.as_view(), name='cart-checkout'),
    path('textilebales/', TextileBaleListCreateAPIView.as_view(), name='textilebale-list-create'),
    path('textilebales/<int:bale_id>/', TextileBaleDetailAPIView.as_view(), name='textilebale-detail'),
    path('salesreport/', SalesReportAPIView.as_view(), name='sales-report'),
    path('productsalesreport/', ProductSalesReportAPIView.as_view(), name='product-sales-report'),
    path('customeractivityreport/', CustomerActivityReportAPIView.as_view(), name='customer-activity-report'),
    path('orderstatusreport/', OrderStatusReportAPIView.as_view(), name='order-status-report'),
]