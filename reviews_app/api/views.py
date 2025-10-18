from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .serializers import ReviewSerializer
from ..models import Review
from.permissions import ReviewPermission
from .filters import ReviewFilter

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, ReviewPermission]
    filter_backends = [DjangoFilterBackend ,filters.OrderingFilter]
    filters_class = ReviewFilter
    ordering_fields = ['updated_at', 'rating']

    # def get_queryset(self):
    #     queryset = Review.objects.all()
    #     business_user_id = self.request.query_params.get('business_user_id')
    #     reviewer_id = self.request.query_params.get('reviewer_id')

    #     if business_user_id:
    #         queryset = queryset.filter(business_user_id=business_user_id)

    #     if reviewer_id:
    #         queryset = queryset.filter(reviewer_id=reviewer_id)
        
    #     return queryset

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)



class ReviewUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, ReviewPermission]

