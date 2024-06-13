from rest_framework import serializers
from .models import Category, Document, SubCategory, Reviews, Location 



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


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"