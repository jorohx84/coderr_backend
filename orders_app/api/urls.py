from django.urls import path
from .views import OrderCreateView, BusinessOrderCountView, CompletedOrderCountView

urlpatterns=[
    path('orders/',OrderCreateView.as_view(), name="orders"),
    path('orders/<int:pk>/', OrderCreateView.as_view(), name="order-detail"),
    path('order-count/<int:business_user_id>/', BusinessOrderCountView.as_view(), name="business-order-count"),
    path('completed-order-count/<int:business_user_id>/', CompletedOrderCountView.as_view(), name="completed-order-count"),
]