from rest_framework import serializers
from .models import Category, Document, SubCategory, Reviews, Location 
from user.models import Gofer, Errand, CustomUser



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        
        
        
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"
        
    # def save(self, **kwargs):
    #     nin = self.validated_data['nin']
    #     bvn = self.validated_data['bvn']
        
    #     return super().save(**kwargs)
        
        
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
    documents = DocumentSerializer(many=True, read_only=True)
    class Meta:
        model = Gofer
        fields = ['id', 'custom_user', 'expertise', 'bio', 'sub_category', 'charges', 'documents']