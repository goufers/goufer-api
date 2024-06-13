from django.contrib import admin
from .models import CustomUser, Gofer, Vendor


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'phone_number']
    
class GoferAdmin(admin.ModelAdmin):
    list_display = ['expertise', 'sub_category']
    
class VendorAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'category']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Gofer, GoferAdmin)
admin.site.register(Vendor, VendorAdmin)