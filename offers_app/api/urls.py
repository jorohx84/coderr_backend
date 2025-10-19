from django.urls import path
from .views import OfferListCreateAPIView, SingleDetailView, OfferRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('offers/', OfferListCreateAPIView.as_view(), name='offer-create'),
    path('offers/<int:pk>/', OfferRetrieveUpdateDestroyAPIView.as_view(), name='offer-detail'),
    path('offerdetails/<int:pk>/', SingleDetailView.as_view(), name='offer-detail'),
]