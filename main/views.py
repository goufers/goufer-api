from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from main.serializers import CategorySerializer, ErrandBoyDocumentSerializer, GoferDocumentSerializer, LocationSerializer, MessagePosterSerializer, SubCategorySerializer, ReviewsSerializer, VendorDocumentSerializer, ErrandSerializer
from user.models import ErrandBoy, Gofer, Vendor
from user.models import Errand
from .models import Category, ErrandBoyDocument, GoferDocument, Location, SubCategory, Reviews, VendorDocument, MessagePoster
from django_filters.rest_framework import DjangoFilterBackend
from main.pagination import CustomPagination
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status



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
    
    
class MessagePosterViewSet(ModelViewSet):
    serializer_class = MessagePosterSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['custom_user__first_name']
    search_fields = ['custom_user__first_name']
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'PATCH']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        logged_in_message_poster_id = MessagePoster.objects.only('id').get(custom_user=user)
        if self.request.user.is_staff:
            return MessagePoster.objects.all()
        return MessagePoster.objects.filter(id=logged_in_message_poster_id)
    
    
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
    filterset_fields = ['message_poster', 'gofer_id', 'rating']
    search_fields = ['gofer_id', 'rating']

    def get_serializer_context(self):
        return {'gofer_id': self.kwargs['gofer_pk']}
    
    # def get_permissions(self):
    #     if self.request.method in ['PUT', 'DELETE', 'PATCH']:
    #         return [IsAdminUser()]
    #     return [IsAuthenticated()]

class ErrandViewSet(ModelViewSet):
    serializer_class = ErrandSerializer
    # permission_classes = [IsAuthenticated]
    queryset = Errand.objects.all()
    
    """perform_create sets the user field to the currently 
    authenticated user and initializes the status to "Ongoing"."""
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status="Ongoing")

    """The update method checks if the requester is either the user who created the errand
      or the gofer assigned to it and allows them to update the errand accordingly."""
    def update(self, request, *args, **kwargs):
        errand = self.get_object()
        if request.user == errand.gofer.custom_user:
            serializer = self.get_serializer(errand, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    """The destroy method allows only the user who created the errand to delete it."""
    def destroy(self, request, *args, **kwargs):
        errand = self.get_object()
        if request.user == errand.user:
            return super().destroy(request, *args, **kwargs)
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    """perform_update method calls the save method of the serializer to apply the changes"""
    def perform_update(self, serializer):
        serializer.save()
    
















    # def get_queryset(self):
    #     user = self.request.user
    #     return Errand.objects.filter(user=user)    
    

    



# from django.shortcuts import render
# from rest_framework.viewsets import ModelViewSet
# from main.serializers import CategorySerializer, DocumentSerializer, LocationSerializer, SubCategorySerializer, ReviewsSerializer, ErrandSerializer, GoferSerializer
# from .models import Category, Document, Location, SubCategory, Reviews
# from user.models import Gofer, Errand
# from django_filters.rest_framework import DjangoFilterBackend
# from main.pagination import CustomPagination
# from rest_framework.filters import SearchFilter
# from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

# # Create your views here.

# class CategoryViewSet(ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     filterset_fields = ['category_name']
#     search_fields = ['category_name']
    
#     def get_permissions(self):
#         if self.request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
#             return [IsAdminUser()]
#         return [AllowAny()]
        
# class DocumentViewSet(ModelViewSet):
#     serializer_class = DocumentSerializer
#     pagination_class = CustomPagination
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     filterset_fields = ['document_type']
#     search_fields = ['document_type']
    
#     def get_permissions(self):
#         if self.request.method in ['PUT', 'DELETE', 'PATCH']:
#             return [IsAdminUser()]
#         return [IsAuthenticated()]
    
#     def get_queryset(self):
#         if self.request.user.is_staff:
#             return Document.objects.all()
#         return Document.objects.filter(custom_user=self.request.user)
    
    
# class LocationViewSet(ModelViewSet):
#     queryset = Location.objects.all()
#     serializer_class = LocationSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     filterset_fields = ['state', 'country']
#     search_fields = ['state', 'country']
    
    
    
# class SubCategoryViewSet(ModelViewSet):
#     serializer_class = SubCategorySerializer
#     def get_queryset(self):
#         return SubCategory.objects.filter(category_id=self.kwargs['category_pk'])
#     def get_serializer_context(self):
#         return {'category_id': self.kwargs['category_pk']}
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     filterset_fields = ['name', 'category_id',]
#     search_fields = ['name']
    
#     def get_permissions(self):
#         if self.request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
#             return [IsAdminUser()]
#         return [AllowAny()]
    
    
    
# class ReviewsViewSet(ModelViewSet):
#     def get_queryset(self):
#         return Reviews.objects.filter(gofer_id=self.kwargs['gofer_pk'])
#     serializer_class = ReviewsSerializer
#     pagination_class = CustomPagination
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     filterset_fields = ['user_id', 'gofer_id', 'rating']
#     search_fields = ['gofer_id', 'rating']
    
#     def get_permissions(self):
#         if self.request.method in ['PUT', 'DELETE', 'PATCH']:
#             return [IsAdminUser()]
#         return [IsAuthenticated()]
