from rest_framework import serializers
from .models import Category, ErrandBoyDocument, GoferDocument, SubCategory, Reviews, Location, VendorDocument 

from .models import Category, Document, SubCategory, Reviews, Location 
from user.models import Gofer, Errand, CustomUser



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        
        
        
class GoferDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoferDocument
        fields = "__all__"
        
class VendorDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDocument
        fields = "__all__"
class ErrandBoyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrandBoyDocument
        fields = "__all__"
        
        
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'description']
        
    def create(self, validated_data):
        category_id = self.context['category_id']
        return SubCategory.objects.create(category_id=category_id, **validated_data)
        
class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"

    def create(self, validated_data):
        gofer_id = self.context["gofer_id"]
        return Reviews.objects.create(gofer_id=gofer_id, **validated_data)


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
        

   
    

    
    


class ErrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Errand
        fields = "__all__"
        read_only_fields = ['created_at','updated_at']

class GoferSerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer()
    documents = GoferDocumentSerializer(many=True, read_only=True)
    class Meta:
        model = Gofer
        fields = ['id', 'custom_user', 'expertise', 'bio', 'sub_category', 'charges', 'documents']