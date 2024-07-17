from django.contrib import admin
from .models import CustomUser, Gofer, Schedule, Vendor, ErrandBoy, Media
from main.models import MessagePoster


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'phone_number', 'phone_verified', 'email_verified']
    search_fields = ['first_name', 'last_name', 'phone_number']
    list_filter = ["gender", 'phone_verified', 'email_verified']
    
    
@admin.register(Gofer)
class GoferAdmin(admin.ModelAdmin):
    list_display = ['expertise', 'sub_category', 'custom_user']
    search_fields = ['custom_user', 'sub_category', 'mobility_means']
    list_filter = ["sub_category", "mobility_means"]
    

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'bio', 'category']
    search_fields = ['business_name', 'category']
    list_filter = ["business_name", "category"]
    
    
@admin.register(ErrandBoy)
class ErrandBoyAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobility_means', 'charges']
    search_fields = ['user', 'mobility_means', 'charges']
    list_filter = ["mobility_means"]

@admin.register(MessagePoster)
class MessagePosterAdmin(admin.ModelAdmin):
    list_display = ['custom_user']
    search_fields = ['custom_user']
    list_filter = ["custom_user"]

@admin.register(Media)
class Media(admin.ModelAdmin):
    list_display = ['vendor', 'media']



@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['id','pro_gofer', 'day_of_week_available', 'start_time_available', 'end_time_available', 'created_at']
    search_fields = ['pro_gofer', 'day', 'from_hour', 'to_hour']
    list_select_related = ['pro_gofer']
    list_filter = ['created_at']
    list_per_page = 10