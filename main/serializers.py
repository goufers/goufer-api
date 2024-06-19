from rest_framework import serializers

from .models import Category, Contract, Document, SubCategory, Reviews, Location 
from datetime import datetime



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
        
class ContractSerializer(serializers.ModelSerializer):
    days_remaining = serializers.SerializerMethodField(method_name="calculate_days_remaining")
    contract_length_in_days = serializers.SerializerMethodField(method_name="calculate_contract_length")
   
    class Meta:
        model = Contract
        fields = ["id", "pay_rate", "scope_of_work", "start_date", "end_date", "contract_length_in_days", "days_remaining", "contract_status", "created_at", "updated_at"]
        
    def calculate_contract_length(self, contract:Contract):
        # start_date = self.validated_data["start_date"]
        # end_date = self.validated_data["end_date"]
        # start = datetime(start_date)
        # end = datetime(end_date)
        # difference = end - start
        # return difference.days
    
        difference = datetime(contract.end_date) - datetime(contract.start_date)
        return difference.days
    

    def calculate_days_remaining(self, contract:Contract):
        remaining_days = datetime(contract.end_date) - datetime.now()
        return remaining_days.days
    
    def create(self, validated_data):
        gofer_id = self.context['gofer_id']
        
        return Contract.objects.create(gofer_id=gofer_id, **validated_data)