from django.urls import path
from .views import SingleProfileView, BusinessAndCustomerProfileView

urlpatterns = [
    path('profile/<int:pk>/', SingleProfileView.as_view(), name="profile-detail"),
    path('profiles/<str:type>/', BusinessAndCustomerProfileView.as_view(), name="business-profile"),
 
]