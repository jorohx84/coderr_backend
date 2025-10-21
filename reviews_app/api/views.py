from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated
from .filters import ReviewFilter
from .permissions import ReviewPermission
from .serializers import ReviewSerializer
from ..models import Review

class ReviewListCreateView(generics.ListCreateAPIView):
    """
    API endpoint that allows reviews to be listed or created.

    Features:
    - Lists all reviews, optionally filtered by 'business_user_id' or 'reviewer_id' via query parameters.
    - Supports ordering by 'updated_at' and 'rating' fields.
    - Only authenticated users can access this endpoint.
    - Permission restrictions:
        - Only users with type 'customer' can create reviews.
        - Only the reviewer who created a review can update or delete it.
    - When creating a review, the 'reviewer' field is automatically set to the current authenticated user.

    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, ReviewPermission]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class= ReviewFilter
    ordering_fields = ['updated_at', 'rating']

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)



class ReviewUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """

    API endpoint to retrieve, update, or delete a single review by its ID.

    Permissions:
    - Only authenticated users can access this endpoint.
    - Only the original reviewer (creator) of the review is allowed to update or delete it.

    Usage:
    - GET: Retrieve the review details.
    - PATCH/PUT: Update the review (only allowed for the creator).
    - DELETE: Delete the review (only allowed for the creator).

    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, ReviewPermission]

