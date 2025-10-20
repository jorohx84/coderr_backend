from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from auth_app.models import CustomUser
from offers_app.models import Feature, OfferDetail
from orders_app.models import Order
from .permissions import OrderPermission
from .serializers import OrderSerializer


class OrderCreateView(APIView):
    """

    API view to handle listing, creating, updating, and deleting orders.

    Methods:
    - GET: List all existing orders.
    - POST: Create a new order linked to a specific offer detail.
        Requires 'offer_detail_id' in the request data.
        Sets customer as the authenticated user and assigns related business user from the offer.
        Automatically assigns features from the offer detail.
    - PATCH: Partially update an existing order by its ID.
    - DELETE: Delete an existing order by its ID.

    Permissions:
    - User must be authenticated.
    - Additional permissions handled by OrderPermission class:
        - POST allowed only for users of type 'customer'.
        - PATCH allowed only for users of type 'business'.
        - DELETE allowed only for admin users (is_staff).

    Note:
    - PATCH and DELETE require 'pk' parameter in the URL for order identification.

    """
    permission_classes = [IsAuthenticated, OrderPermission]

    def get(self, request):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        offer_detail_id = request.data.get("offer_detail_id")
        if not offer_detail_id:
            return Response({"error":"offer_detail_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        offer_detail = get_object_or_404(OfferDetail.objects.select_related('offer'), id=offer_detail_id)
          
        order = Order.objects.create(
            customer_user=request.user,
            business_user=offer_detail.offer.user,
            title=offer_detail.offer.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            offer_type=offer_detail.offer_type,
            offer_detail=offer_detail,
        )

        feature_names = offer_detail.features 
        feature_objects = []

        for name in feature_names:
            feature_obj, _ = Feature.objects.get_or_create(name=name)
            feature_objects.append(feature_obj)


        order.features.set(feature_objects)

        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error":"Order not found"}, status=status.HTTP_404_NOT_FOUND)
        

        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error":"Order not found"}, status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

       

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