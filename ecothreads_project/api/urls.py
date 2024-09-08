from django.urls import path
from .views import ProductsListView, ProductsDetailView
from .views import TextileBaleListCreateView, TextileBaleDetailView
from .views import OrderListCreateView, OrderDetailView, CartCheckoutView
from .views import FootAgentListCreateView, FootAgentDetailView
from .views import AgentAssignmentListCreateView, AgentAssignmentDetailView


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
]

