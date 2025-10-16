# urls.py
# from django.urls import path
# from .views import OfferCreateView

# urlpatterns = [
#     path('offers/', OfferCreateView.as_view(), name='offer-create'),
# ]
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OfferViewSet, OfferDetailsViewSet

router = DefaultRouter()
router.register(r'offers', OfferViewSet)
router.register(r'offerdetails', OfferDetailsViewSet)


urlpatterns = router.urls