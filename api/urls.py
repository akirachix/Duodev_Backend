from django.urls import path
from .views import (
    # Product-related views
    ProductsListView, ProductsDetailView,

    # Textile bale-related views
    TextileBaleListView, TextileBaleDetailView,

    # Order-related views
    OrderListCreateAPIView, OrderDetailAPIView, CartCheckoutView,

    # Foot Agent-related views
    FootAgentListCreateView, FootAgentDetailView,
    AgentAssignmentListCreateView, AgentAssignmentDetailView,

    # Company-related views
    CompanySignUpView, CompanySignInView,

    # Other reports/views
    UserRegistrationView,  TopSoldProductOfWeekAPIView,
    TradersInteractedAPIView,SellersAPIView,
    TotalSalesAPIView, send_invitation_email, UserLoginView
)

urlpatterns = [
    # Product-related URLs
    path('products/', ProductsListView.as_view(), name='products-list'),
    path('products/<int:pk>/', ProductsDetailView.as_view(), name='products-detail'),
    

    # Textile bale-related URLs
    path('textilebales/', TextileBaleListView.as_view(), name='textilebale-list'),
    path('textilebale/<int:bale_id>/', TextileBaleDetailView.as_view(), name='textilebale-detail'),

    # Order-related URLs
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:id>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('cart/checkout/', CartCheckoutView.as_view(), name='cart-checkout'),

    # Foot Agent-related URLs
    path('footagents/', FootAgentListCreateView.as_view(), name='footagent-list'),
    path('footagents/<int:pk>/', FootAgentDetailView.as_view(), name='footagent-detail'),
    path('agent-assignments/', AgentAssignmentListCreateView.as_view(), name='agentassignment-list-create'),
    path('agent-assignments/<int:pk>/', AgentAssignmentDetailView.as_view(), name='agentassignment-detail'),

    # Company-related URLs
    path('company/signup/', CompanySignUpView.as_view(), name='company_signup'),
    path('company/signin/', CompanySignInView.as_view(), name='company_signin'),

    # User registration and reports
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('top-sold-product-of-week/', TopSoldProductOfWeekAPIView.as_view(), name='top-sold-product-of-week'),
    path('traders-interacted/', TradersInteractedAPIView.as_view(), name='traders-interacted'),
    path('sellers/', SellersAPIView.as_view(), name='sellers'),
    path('total-sales/', TotalSalesAPIView.as_view(), name='total-sales'),

    # Invitation
    path('send-invitation/', send_invitation_email, name='send_invitation'),
    
    #Login
    path('login/', UserLoginView.as_view(), name='login'),   
]
