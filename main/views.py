from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from main.serializers import CategorySerializer, DocumentSerializer, LocationSerializer, SubCategorySerializer, ReviewsSerializer
from .models import Category, Document, Location, SubCategory, Reviews
from django_filters.rest_framework import DjangoFilterBackend
from main.pagination import CustomPagination
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

# Create your views here.

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
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
        if self.request.user.is_staff:
            return Document.objects.all()
        return Document.objects.filter(custom_user=self.request.user)
    
    
class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['state', 'country']
    search_fields = ['state', 'country']
    
    
    
class SubCategoryViewSet(ModelViewSet):
    serializer_class = SubCategorySerializer
    def get_queryset(self):
        return SubCategory.objects.filter(category_id=self.kwargs['category_pk'])
    def get_serializer_context(self):
        return {'category_id': self.kwargs['category_pk']}
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'category_id',]
    search_fields = ['name']
    
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


