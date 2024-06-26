from django.contrib import admin
from .models import Bank, Wallet, Transaction, Schedule, ProGofer, Booking


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['pro_gofer', 'day', 'from_hour', 'to_hour']
    search_fields = ['pro_gofer', 'day', 'from_hour', 'to_hour']
    list_select_related = ['pro_gofer']
    list_filter = ['created_at']
    list_per_page = 10


class BankAdmin(admin.ModelAdmin):
    list_display = ['custom_user', 'recipient_code', 'bank_name', 'account_number', 'created_at', 'updated_at']
    search_fields = ['custom_user', 'recipient_code', 'bank_name', 'account_number']
    list_filter = ['created_at', 'updated_at']


class WalletAdmin(admin.ModelAdmin):
    list_display = ['custom_user', 'transaction_pin', 'balance', 'created_at']
    search_fields = ['custom_user', 'transaction_pin', 'balance']
    list_filter = ['created_at']

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'amount', 'transaction_type', 'created_at']
    search_fields = ['wallet', 'amount', 'transaction_type']
    list_filter = ['created_at']
    list_select_related = ['wallet']
    list_per_page = 10

@admin.register(ProGofer)
class ProGoferAdmin(admin.ModelAdmin):
    list_display = ['custom_user', 'bio', 'profession', 'hourly_rate', 'is_verified', 'created_at', 'updated_at']
    search_fields = ['custom_user', 'bio', 'profession', 'hourly_rate', 'is_verified']
    list_filter = ['created_at', 'updated_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['message_poster', 'pro_gofer', 'schedule', 'duration', 'status']
    search_fields = ['message_poster', 'pro_gofer', 'is_active', 'duration']
    list_filter = ['booked_at']
    list_select_related = ['message_poster', 'pro_gofer']
    list_per_page = 10
    list_display_links = ['message_poster', 'pro_gofer', 'status']



admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(Schedule, ScheduleAdmin)
