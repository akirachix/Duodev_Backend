from django.urls import path
from .views import (
    ProductsListView, ProductsDetailView,
    UserRegistrationView,
    OrderListCreateAPIView, OrderDetailAPIView, CartCheckoutAPIView,
    TextileBaleListCreateAPIView, TextileBaleDetailAPIView,
    SalesReportAPIView, ProductSalesReportAPIView,
    OrderStatusReportAPIView, CustomerActivityReportAPIView
)
urlpatterns = [
    # Products URLs
    path('products/', ProductsListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductsDetailView.as_view(), name='product_detail'),

    # User Registration URL
    path('register/', UserRegistrationView.as_view(), name='register'),

    # Order URLs
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:order_id>/', OrderDetailAPIView.as_view(), name='order-detail'),

    # Cart Checkout URL
    path('cart/checkout/', CartCheckoutAPIView.as_view(), name='cart-checkout'),

    # Textile Bale URLs
    path('textilebales/', TextileBaleListCreateAPIView.as_view(), name='textilebale-list-create'),
    path('textilebales/<int:bale_id>/', TextileBaleDetailAPIView.as_view(), name='textilebale-detail'),
    
    # Reporting URLs
    path('reports/sales/', SalesReportAPIView.as_view(), name='sales-report'),
    path('reports/product-sales/', ProductSalesReportAPIView.as_view(), name='product-sales-report'),
    path('reports/order-status/', OrderStatusReportAPIView.as_view(), name='order-status-report'),
    path('reports/customer-activity/', CustomerActivityReportAPIView.as_view(), name='customer-activity-report'),
]