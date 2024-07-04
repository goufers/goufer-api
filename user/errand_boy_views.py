from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ErrandBoySerializer
from .models import ErrandBoy


class ErrandBoyViewset(ModelViewSet):
    queryset = ErrandBoy.objects.all()
    serializer_class = ErrandBoySerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    
    def update(self, request, pk):
        errand_boy = ErrandBoy.objects.get(pk=pk)
        serializer = ErrandBoySerializer(data=request.data, instance=errand_boy, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
