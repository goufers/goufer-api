from rest_framework import serializers
from .models import Address, Category, Document, SubCategory, Reviews, Location 


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        
        
        
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "document_type", "document_number", "document_of_expertise", "uploaded_at", "is_verified"]
        
    def create(self, validated_data):
        currently_logged_in_user_id = self.context["currently_logged_in_user_id"]
        return Document.objects.create(user_id=currently_logged_in_user_id, **validated_data)
        

        

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


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
        
        
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        
        


        

   
    

    
    