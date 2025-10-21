from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from auth_app.models import CustomUser
from offers_app.models import Feature, OfferDetail
from orders_app.models import Order
from .permissions import OrderPermission
from .serializers import OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    """
    API view to list all orders and create a new order.

    GET:
        - Returns a list of all orders.
        - Requires the user to be authenticated.

    POST:
        - Creates a new order linked to a specific OfferDetail.
        - Requires 'offer_detail_id' in the request data.
        - Only users with user.type == 'customer' are permitted to create orders.
        - Automatically assigns features from the referenced OfferDetail.
        - Validates that 'offer_detail_id' is an integer and corresponds to an existing OfferDetail.
    
    Permissions:
        - User must be authenticated.
        - Permission class OrderPermission enforces user type restrictions.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, OrderPermission]

    def perform_create(self, serializer):
        offer_detail_id = self.request.data.get("offer_detail_id")
        if not offer_detail_id:
            raise ValidationError({"offer_detail_id": "This field is required."})

        try:
            offer_detail_id = int(offer_detail_id)
        except (ValueError, TypeError):
            raise ValidationError({"offer_detail_id": "Must be an integer."})

        offer_detail = OfferDetail.objects.select_related('offer').filter(id=offer_detail_id).first()
        if not offer_detail:
            raise ValidationError({"offer_detail_id": "OfferDetail with this ID does not exist."})

        feature_names = offer_detail.features
        feature_objects = []
        for name in feature_names:
            feature_obj, _ = Feature.objects.get_or_create(name=name)
            feature_objects.append(feature_obj)

        order = serializer.save(
            customer_user=self.request.user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            offer_type=offer_detail.offer_type,
            offer_detail=offer_detail,
        )
        order.features.set(feature_objects)      


class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, partially update, or delete an individual order by ID.

    GET:
        - Retrieve details of a single order.
        - Requires the user to be authenticated.

    PATCH:
        - Partially updates the specified order.
        - Only users with user.type == 'business' are permitted to update orders.

    DELETE:
        - Deletes the specified order.
        - Only admin users (user.is_staff == True) are permitted to delete orders.

    Permissions:
        - User must be authenticated.
        - Permission class OrderPermission enforces method- and object-level permissions.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, OrderPermission]




class BusinessOrderCountView(APIView):
    """

    API endpoint to retrieve the count of 'in progress' orders for a specific business user.

    URL Parameter:
    - business_user_id (int): The ID of the business user.

    Permissions:
    - Requires authenticated user.

    Behavior:
    - Validates that the business user exists and has type 'business'.
    - Returns the count of orders assigned to the business user with status 'in progress'.
    - If the business user does not exist or is not of type 'business', returns 404 error.

    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        try:
            business_user = CustomUser.objects.get(id=business_user_id, type='business')
        except CustomUser.DoesNotExist:
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)

        count = Order.objects.filter(business_user=business_user, status='in progress').count()
        return Response({"order_count": count}, status=status.HTTP_200_OK)
    

class CompletedOrderCountView(APIView):
    """

    API endpoint to retrieve the count of 'completed' orders for a specific business user.

    URL Parameter:
    - business_user_id (int): The ID of the business user.

    Permissions:
    - Requires authenticated user.

    Behavior:
    - Validates that the business user exists and has type 'business'.
    - Returns the count of orders assigned to the business user with status 'completed'.
    - If the business user does not exist or is not of type 'business', returns 404 error.

    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        try:
            business_user = CustomUser.objects.get(id=business_user_id, type='business')
        except CustomUser.DoesNotExist:
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)

        count = Order.objects.filter(business_user=business_user, status='completed').count()
        return Response({"completed_order_count": count}, status=status.HTTP_200_OK)