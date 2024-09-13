from django.urls import path
from .views import (
    # Product-related views
    ProductsListView, ProductsDetailView,

    # Textile bale-related views
    TextileBaleListCreateView, TextileBaleDetailView,

    # Order-related views
    OrderListCreateView, OrderDetailAPIView, CartCheckoutView,

    # Foot Agent-related views
    FootAgentListCreateView, FootAgentDetailView,
    AgentAssignmentListCreateView, AgentAssignmentDetailView,

    # Company-related views
    CompanySignUpView, CompanySignInView,

    # Other reports/views
    UserRegistrationView, SalesReportAPIView, ProductSalesReportAPIView, 
    CustomerActivityReportAPIView, OrderStatusReportAPIView, send_invitation_email
)

urlpatterns = [
    # Product-related URLs
    path('products/', ProductsListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductsDetailView.as_view(), name='product_detail'),

    # Textile bale-related URLs
    path('textilebale/', TextileBaleListCreateView.as_view(), name='textilebale-list-create'),
    path('textilebale/<int:bale_id>/', TextileBaleDetailView.as_view(), name='textilebale-detail'),

    # Order-related URLs
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:id>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('cart/checkout/', CartCheckoutView.as_view(), name='cart-checkout'),

    # Foot Agent-related URLs
    path('footagents/', FootAgentListCreateView.as_view(), name='footagent-list-create'),
    path('footagents/<int:agent_id>/', FootAgentDetailView.as_view(), name='footagent-detail'),
    path('footagents/assignments/', AgentAssignmentListCreateView.as_view(), name='assignment-list-create'),
    path('footagents/assignments/<int:assignment_id>/', AgentAssignmentDetailView.as_view(), name='assignment-detail'),

    # Company-related URLs
    path('company/signup/', CompanySignUpView.as_view(), name='company_signup'),
    path('company/signin/', CompanySignInView.as_view(), name='company_signin'),

    # User registration and reports
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('salesreport/', SalesReportAPIView.as_view(), name='sales-report'),
    path('productsalesreport/', ProductSalesReportAPIView.as_view(), name='product-sales-report'),
    path('customeractivityreport/', CustomerActivityReportAPIView.as_view(), name='customer-activity-report'),
    path('orderstatusreport/', OrderStatusReportAPIView.as_view(), name='order-status-report'),

    # Invitation
    path('send-invitation/', send_invitation_email, name='send_invitation'),
]
