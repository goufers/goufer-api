from django.contrib import admin
from .models import Location, Category, SubCategory, Document, Reviews
from user.models import Errand, Gofer
from django.utils.html import format_html, urlencode
from django.db.models import Count
from django.urls import reverse





@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['latitude', 'longitude', 'address', 'state', 'country']
    search_fields = ['address', 'state', 'country']
    list_filter = ['state', 'country']
    list_per_page = 10
     
     
     
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'description']
    search_fields = ['name__istartswith']
    list_filter = ['category', 'name']
    list_per_page = 10
    list_select_related = ['category']
    
    
class SubCategoryInline(admin.StackedInline):
    model = SubCategory

# @admin.register(Document)
# class DocumentAdmin(admin.ModelAdmin):
#     list_display = ['document_type', 'message_poster', 'document_of_expertise', 'uploaded_at', 'is_verified']
#     search_fields = ['document_type__istartswith']
#     list_filter = ['document_type']
#     list_per_page = 10
    


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'description', 'created_at', 'sub_category_count']
    search_fields = ['category_name__istartswith']
    list_filter = ['category_name']
    list_per_page = 10
    inlines = [SubCategoryInline]
    
    def sub_category_count(self, category: Category):
        url = (reverse('admin:main_subcategory_changelist') +
               '?' + 
               urlencode({"category__id": str(category.id)}))
        return format_html("<a href='{}'>{}</a>", url, category.sub_category_count)
    
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(sub_category_count=Count("sub_categories"))
    


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['message_poster', 'gofer', 'comment', 'rating', 'date']
    search_fields = ['user__istartswith', 'gofer__istartswith', 'rating ']
    list_filter = ['message_poster', 'gofer', 'rating', 'date']
    list_per_page = 10
    list_select_related = ['user', 'gofer']
    
@admin.register(Gofer)
class GoferAdmin(admin.ModelAdmin):
    list_display = ['expertise', 'sub_category']
    search_fields = ['custom_user', 'expertise', 'sub_category', 'charges']
    list_filter = ['custom_user', 'expertise']
    list_per_page = 20



@admin.register(Errand) 
class ErrandAdmin(admin.ModelAdmin):
    list_display = ['user', 'task_description', 'sub_category', 'gofer', 'estimated_duration', 'status']
    search_fields = ['user', 'gofer', 'sub_category']
    list_filter = ['user', 'gofer', 'sub_category']
    list_per_page = 10
    list_select_related =['user', 'gofer']