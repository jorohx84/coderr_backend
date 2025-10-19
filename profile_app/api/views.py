from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Profile
from .permissions import IsProfileOwner
from .serializers import BusinessProfileSerializer, CustomerProfileSerializer, ProfileSerializer

     

class BusinessAndCustomerProfileView(generics.ListAPIView):
    """
    View: BusinessAndCustomerProfileView

    Description:
    Returns a list of user profiles filtered by type ('customer' or 'business').
    The serializer used depends on the type provided via the URL parameter.

    Permissions:
    - Only accessible to authenticated users.


    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        type = self.kwargs.get('type')
        return Profile.objects.filter(type=type)
    
    def get_serializer_class(self):
        profile_type = self.kwargs.get('type')
        if profile_type == 'customer':
            return CustomerProfileSerializer
        elif profile_type == 'business':
            return BusinessProfileSerializer

  
class SingleProfileView(generics.RetrieveUpdateAPIView):
    """
    View: SingleProfileView

    Description:
    Retrieves or updates a single user's profile.
    Only the owner of the profile is allowed to update it.

    Permissions:
    - User must be authenticated (IsAuthenticated).
    - User must be the owner of the profile (IsProfileOwner).

    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            profile =  Profile.objects.get(user=pk)
        except Profile.DoesNotExist:
           raise NotFound("Profile not found")
        
        self.check_object_permissions(self.request, profile)
                                      
        return profile
    
