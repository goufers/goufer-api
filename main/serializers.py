from rest_framework import serializers
from .models import Category, ErrandBoyDocument, GoferDocument, SubCategory, Reviews, Location, VendorDocument, ProGoferDocument, MessagePoster, Address

from .models import Category, Document, SubCategory, Reviews, Location 
from user.models import Gofer, Errand, CustomUser



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
        


class MessagePosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessagePoster
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
        gofer_id = self.context['gofer_id']
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


class ErrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Errand
        fields = ['id', 'user', 'task_description', 'sub_category', 'gofer', 'estimated_duration', 'status', 'created_at', 'updated_at', 'errand_accepted']
        read_only_fields = ['user', 'status', 'created_at', 'updated_at', 'errand_accepted']

    def update(self, instance, validated_data):
        if 'errand_accepted' in validated_data and validated_data['errand_accepted'] is not None:
            instance.errand_accepted = validated_data['errand_accepted']
            if instance.errand_accepted:
                instance.status = "Ongoing"
            else:
                instance.status = "Terminated"
        instance.task_description = validated_data.get('task_description', instance.task_description)
        instance.sub_category = validated_data.get('sub_category', instance.sub_category)
        instance.estimated_duration = validated_data.get('estimated_duration', instance.estimated_duration)
        instance.save()
        return instance
    
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['house_number', 'street', 'city', 'state', 'country']