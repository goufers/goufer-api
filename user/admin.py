from django.contrib import admin
from .models import CustomUser, Gofer, Vendor, ErrandBoy


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'phone_number', 'phone_verified', 'email_verified']
    
class GoferAdmin(admin.ModelAdmin):
    list_display = ['expertise', 'sub_category']
    
class VendorAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'bio', 'category']
    
class ErrandBoyAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobility_means', 'charges']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Gofer, GoferAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(ErrandBoy, ErrandBoyAdmin)