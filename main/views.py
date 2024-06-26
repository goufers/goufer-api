from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from main.serializers import CategorySerializer, ErrandBoyDocumentSerializer, GoferDocumentSerializer, LocationSerializer, SubCategorySerializer, ReviewsSerializer, VendorDocumentSerializer
from user.models import ErrandBoy, Gofer, Vendor
from .models import Category, ErrandBoyDocument, GoferDocument, Location, SubCategory, Reviews, VendorDocument
from django_filters.rest_framework import DjangoFilterBackend
from main.pagination import CustomPagination
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny



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
        
class GoferDocumentViewSet(ModelViewSet):
    serializer_class = GoferDocumentSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['document_type']
    search_fields = ['document_type']
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'PATCH']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        logged_in_gofer = Gofer.objects.only('id').get(custom_user=user)
        if self.request.user.is_staff:
            return GoferDocument.objects.all()
        return GoferDocument.objects.filter(gofer_id=logged_in_gofer)
    
    
class VendorDocumentViewSet(ModelViewSet):
    serializer_class = VendorDocumentSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['document_type']
    search_fields = ['document_type']
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'PATCH']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self): 
        user = self.request.user
        logged_in_vendor = Vendor.objects.only('id').get(custom_user=user)
        if self.request.user.is_staff:
            return VendorDocument.objects.all()
        return VendorDocument.objects.filter(vendor_id=logged_in_vendor)
    
    
class ErrandBoyDocumentViewSet(ModelViewSet):
    serializer_class = ErrandBoyDocumentSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['document_type']
    search_fields = ['document_type']
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'PATCH']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        logged_in_errand_boy = ErrandBoy.objects.only('id').get(user=user)
        if self.request.user.is_staff:
            return ErrandBoyDocument.objects.all()
        return ErrandBoyDocument.objects.filter(gofer_id=logged_in_errand_boy)
    
    
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
    
    

    



from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from main.serializers import CategorySerializer, DocumentSerializer, LocationSerializer, SubCategorySerializer, ReviewsSerializer, ErrandSerializer, GoferSerializer
from .models import Category, Document, Location, SubCategory, Reviews
from user.models import Gofer, Errand
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


class ErrandViewSet(ModelViewSet):
    serializer_class = ErrandSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'PATCH']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        return Errand.objects.filter(user=user)

class GoferViewSet(ModelViewSet):
    queryset = Gofer.objects.all()
    serializer_class = GoferSerializer
    permission_classes = [IsAuthenticated]