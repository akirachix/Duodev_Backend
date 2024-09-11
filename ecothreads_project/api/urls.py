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
from .views import ProductsListView, ProductsDetailView
from .views import TextileBaleListCreateView, TextileBaleDetailView
from .views import OrderListCreateView, OrderDetailView, CartCheckoutView
from .views import FootAgentListCreateView, FootAgentDetailView
from .views import AgentAssignmentListCreateView, AgentAssignmentDetailView
from .views import CompanySignUpView, CompanySignInView
from .views import send_invitation_email


urlpatterns = [
    path('products/', ProductsListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductsDetailView.as_view(), name='product_detail'),
    path('textilebale/', TextileBaleListCreateView.as_view(), name='textilebale-list-create'),
    path('textilebale/<int:bale_id>/', TextileBaleDetailView.as_view(), name='textilebale-detail'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('cart/checkout/', CartCheckoutView.as_view(), name='cart-checkout'),
    path('footagents/', FootAgentListCreateView.as_view(), name='footagent-list-create'),
    path('footagents/<int:agent_id>/', FootAgentDetailView.as_view(), name='footagent-detail'),
    path('footagents/assignments/', AgentAssignmentListCreateView.as_view(), name='assignment-list-create'),
    path('footagents/assignments/<int:assignment_id>/', AgentAssignmentDetailView.as_view(), name='assignment-detail'),
    path('company/signup/', CompanySignUpView.as_view(), name='company_signup'),
    path('company/signin/', CompanySignInView.as_view(), name='company_signin'),
    path('send-invitation/', send_invitation_email, name='send_invitation'),
]

