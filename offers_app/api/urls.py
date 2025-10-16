# urls.py
# from django.urls import path
# from .views import OfferCreateView

# urlpatterns = [
#     path('offers/', OfferCreateView.as_view(), name='offer-create'),
# ]
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OfferViewSet, OfferDetailView

router = DefaultRouter()
router.register(r'offers', OfferViewSet, basename='offer')

urlpatterns = router.urls + [
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name="offer-detail"),
]
