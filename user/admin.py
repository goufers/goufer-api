from django.contrib import admin
from .models import CustomUser, Gofer, Vendor, ErrandBoy


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'phone_number', 'phone_verified', 'email_verified']
    search_fields = ['first_name', 'last_name', 'phone_number']
    list_filter = ["gender", 'phone_verified', 'email_verified']
    
class GoferAdmin(admin.ModelAdmin):
    list_display = ['expertise', 'sub_category']
    search_fields = ['custom_user', 'sub_category', 'mobility_means']
    list_filter = ["sub_category", "mobility_means"]
    
class VendorAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'bio', 'category']
    search_fields = ['business_name', 'category']
    list_filter = ["business_name", "category"]
    
    
class ErrandBoyAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobility_means', 'charges']
    search_fields = ['user', 'mobility_means', 'charges']
    list_filter = ["mobility_means"]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Gofer, GoferAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(ErrandBoy, ErrandBoyAdmin)