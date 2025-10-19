from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from ..models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferListSerializer, OfferDetailSerializer, SingleOfferSerializer, OfferUpdateSerializer
from .permissions import OfferPermission
from .filters import OfferFilter

class OfferPagination(PageNumberPagination):
    """

    Custom pagination class for Offer API endpoints.
    - Default page size: 10
    - Client can specify page size with 'page_size' query param
    - Maximum allowed page size: 100

    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class OfferListCreateAPIView(generics.ListCreateAPIView):
    """

    API endpoint for listing all offers and creating new offers.

    Features:
    - Queryset optimized with prefetch_related for 'details' and 'user'
    - Permissions: authenticated users with OfferPermission
    - Supports filtering (via OfferFilter), ordering, and search
    - Pagination with OfferPagination
    - Serializer:
        - POST requests use OfferSerializer for creation
        - GET requests use OfferListSerializer for listing

    """
    queryset = Offer.objects.all().prefetch_related('details', 'user')
    permission_classes = [IsAuthenticated, OfferPermission]

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
    """

    API endpoint for retrieving, updating, or deleting a single offer.

    Features:
    - Permissions: authenticated users with OfferPermission
    - Serializer:
        - PATCH/PUT requests use OfferUpdateSerializer for updates
        - GET requests use SingleOfferSerializer for detail retrieval

    """
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated, OfferPermission]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return OfferUpdateSerializer
        return SingleOfferSerializer

class SingleDetailView(generics.RetrieveAPIView):
    """

    API endpoint to retrieve a single OfferDetail instance.

    Features:
    - Requires authentication
    - Uses OfferDetailSerializer for serialization
    
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]



