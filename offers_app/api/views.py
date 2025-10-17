from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from ..models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferListSerializer, OfferDetailSerializer, SingleOfferSerializer, OfferUpdateSerializer
from .permissions import IsBusinessUser, IsCreator
from .filters import OfferFilter

class OfferPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class OfferListCreateAPIView(generics.ListCreateAPIView):
    queryset = Offer.objects.all().prefetch_related('details', 'user')
    permission_classes = [IsAuthenticated, IsBusinessUser]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'min_price']
    search_fields = ['title', 'description']
    pagination_class = OfferPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferSerializer
        return OfferListSerializer

    def perform_create(self, serializer):
        serializer.save()


class OfferRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated, IsCreator, IsBusinessUser]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return OfferUpdateSerializer
        return SingleOfferSerializer

class SingleDetailView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]



