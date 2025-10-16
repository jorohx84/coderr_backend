# urls.py
# from django.urls import path
# from .views import OfferCreateView

# urlpatterns = [
#     path('offers/', OfferCreateView.as_view(), name='offer-create'),
# ]
from rest_framework.routers import DefaultRouter
from .views import OfferViewSet

router = DefaultRouter()
router.register(r'offers', OfferViewSet, basename='offer')

urlpatterns = router.urls
