from .serializers import VendorCreateSerializer, VendorSerializer
from rest_framework import viewsets
from .models import Vendor
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
    
    def update(self, request, pk):
        vendor = Vendor.objects.get(id=pk)
        serializer = VendorSerializer(data=request.data, instance=vendor, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return VendorCreateSerializer
        return VendorSerializer
