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
from .serializers import OrderSerializer, OrderCreateInputSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    """
    API endpoint to list all orders (GET) and create a new order (POST).

    GET:
        - Returns a list of all orders.
        - Requires the user to be authenticated.
        - Uses OrderSerializer for response data.

    POST:
        - Creates a new order based on a given OfferDetail.
        - Request body must include: {"offer_detail_id": <int>}
        - Only users with user.type == "customer" are allowed to create orders.
        - Automatically copies relevant fields from the OfferDetail:
            - title, revisions, delivery_time_in_days, price, offer_type
        - Features from the OfferDetail are added to the order (created if necessary).
        - Returns the full created order using OrderSerializer.

    Permissions:
        - All actions require authentication (IsAuthenticated).
        - OrderPermission ensures only 'customer' users can create orders.
    """
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, OrderPermission]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateInputSerializer  
        return OrderSerializer 

    def create(self, request, *args, **kwargs):
        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        offer_detail_id = input_serializer.validated_data['offer_detail_id']

        try: offer_detail_id = int(offer_detail_id) 
        except (ValueError, TypeError): 
            raise ValidationError({"offer_detail_id": "Must be an integer."})

        offer_detail = OfferDetail.objects.select_related('offer').filter(id=offer_detail_id).first() 
        if not offer_detail: 
            raise ValidationError({"offer_detail_id": "OfferDetail with this ID does not exist."})
        

        feature_objects = []
        for name in offer_detail.features:
            feature, _ = Feature.objects.get_or_create(name=name)
            feature_objects.append(feature)

        order = Order.objects.create(
            customer_user=request.user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            offer_type=offer_detail.offer_type,
            offer_detail=offer_detail,
            status="in_progress",
        )
        order.features.set(feature_objects)

        output_serializer = OrderSerializer(order)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    


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