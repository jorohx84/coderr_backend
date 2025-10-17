from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer
from orders_app.models import Order
from offers_app.models import OfferDetail, Feature
from .permissions import OrderPermission
from auth_app.models import CustomUser


class OrderCreateView(APIView):
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
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            offer_type=offer_detail.offer_type,
            offer_detail=offer_detail,
        )

        # ✅ Wichtig: JSON-Features in echte Feature-Modelle umwandeln
        feature_names = offer_detail.features  # z.B. ["Logo Design", "Flyer"]
        feature_objects = []

        for name in feature_names:
            feature_obj, _ = Feature.objects.get_or_create(name=name)
            feature_objects.append(feature_obj)

    # ✅ ManyToMany-Feld korrekt befüllen
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
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        try:
            business_user = CustomUser.objects.get(id=business_user_id, type='business')
        except CustomUser.DoesNotExist:
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)

        count = Order.objects.filter(business_user=business_user, status='in progress').count()
        return Response({"order_count": count}, status=status.HTTP_200_OK)
    

class CompletedOrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        try:
            business_user = CustomUser.objects.get(id=business_user_id, type='business')
        except CustomUser.DoesNotExist:
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)

        count = Order.objects.filter(business_user=business_user, status='completed').count()
        return Response({"completed_order_count": count}, status=status.HTTP_200_OK)