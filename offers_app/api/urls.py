
# from django.urls import path
# from rest_framework.routers import DefaultRouter
# from .views import OfferViewSet

# router = DefaultRouter()
# router.register(r'offers', OfferViewSet)



# urlpatterns = router.urls

from django.urls import path
from .views import OfferListCreateAPIView, SingleDetailView, OfferRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('offers/', OfferListCreateAPIView.as_view(), name='offer-create'),
    path('offers/<int:pk>/', OfferRetrieveUpdateDestroyAPIView.as_view(), name='offer-detail'),
    path('offerdetails/<int:pk>/', SingleDetailView.as_view(), name='offer-detail'),
]