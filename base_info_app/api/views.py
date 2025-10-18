from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BaseInfoSerializer


class BaseInfoView(APIView):
    def get(self, request):
        serializer = BaseInfoSerializer(instance={})
        return Response(serializer.data, status=status.HTTP_200_OK)