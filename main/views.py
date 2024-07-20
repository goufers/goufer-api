from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from main.serializers import AddressSerializer, CategorySerializer, DocumentSerializer, LocationSerializer, SubCategorySerializer, ReviewsSerializer
from user.models import ProGofer
from user.serializers import ProGoferSerializer
from .models import Address, Category, Document, Location, SubCategory, Reviews
from django_filters.rest_framework import DjangoFilterBackend
from main.pagination import CustomPagination
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.prefetch_related('sub_categories').all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category_name']
    search_fields = ['category_name']
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            return [IsAdminUser()]
        return [AllowAny()]
        
class DocumentViewSet(ModelViewSet):
    serializer_class = DocumentSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['document_type']
    search_fields = ['document_type']
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'PATCH']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        currently_logged_in_user = self.request.user
        if self.request.user.is_staff:
            return Document.objects.select_related('user').all()
        return Document.objects.filter(user=currently_logged_in_user)
    
    def get_serializer_context(self):
        return {"currently_logged_in_user_id": self.request.user.id}
    
    
    
    
class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['latitude', 'longitude']
    search_fields = ['latitude', 'longitude']
    
    
class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['city', 'state', 'country',]
    search_fields = ['city', 'state', 'country',]
    
    
    
class SubCategoryViewSet(ModelViewSet):
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'category_id',]
    search_fields = ['name']
    def get_queryset(self):
        return SubCategory.objects.select_related('category').filter(category_id=self.kwargs['category_pk'])
    def get_serializer_context(self):
        return {'category_id': self.kwargs['category_pk']}
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            return [IsAdminUser()]
        return [AllowAny()]
    
    
    
class ReviewsViewSet(ModelViewSet):
    def get_queryset(self):
        return Reviews.objects.filter(gofer_id=self.kwargs['gofer_pk'])
    serializer_class = ReviewsSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user_id', 'gofer_id', 'rating']
    search_fields = ['gofer_id', 'rating']
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'PATCH']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    

    
    



    
    
    

    


