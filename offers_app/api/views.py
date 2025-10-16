from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import filters
from .serializers import OfferSerializer, OfferListSerializer, SinglerOfferSerializer, OfferDetailsSerializer
from ..models import Offer, OfferDetails
from .permissions import IsBusinessUser, IsCreator
from .filters import OfferFilter

class OfferPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.all()
    pagination_class = OfferPagination
    # permission_classes = [IsAuthenticated, IsBusinessUser, IsCreator]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = OfferFilter
    filterset_fields = ['user']
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']

    def get_queryset(self):
        return Offer.objects.annotate(
            min_price=Min('details__price'),
            min_delivery_time=Min('details__delivery_time_in_days')
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return OfferListSerializer
        elif self.action == 'retrieve':
            return SinglerOfferSerializer
        return OfferSerializer
    
    def perform_create(self, serializer):
        serializer.save()

 




class OfferDetailView(generics.RetrieveAPIView):
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailsSerializer