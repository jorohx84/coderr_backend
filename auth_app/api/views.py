from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from ..models import CustomUser
from .serializers import RegistrationSerializer, LoginSerializer

class RegistrationView(generics.ListCreateAPIView):
    """
    API endpoint that allows users to register a new account.

    GET:
        Returns a list of all users (mainly for admin/testing purposes).
    POST:
        Registers a new user with the provided data.
        Returns an authentication token along with basic user info.

    Uses:
    - RegistrationSerializer for validation and user creation.
    """
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
        }, status=status.HTTP_201_CREATED)
    
class LoginView(ObtainAuthToken):
    """
    API endpoint to log in a user.

    POST:
        Validates user credentials.
        Returns an authentication token along with basic user info.

    Uses:
    - LoginSerializer for validation.
    - DRF's TokenAuthentication to generate or retrieve tokens.
    """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, create = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
        }, status=status.HTTP_200_OK)
