# views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import OfferSerializer
from ..models import Offer


class OfferCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print(self.request.user.id)
        serializer.save()
