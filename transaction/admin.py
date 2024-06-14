from django.contrib import admin
from .models import Bank, Wallet, Transaction, Hour, Day, Schedule


class HourAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


class DayAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['user', 'gofer_or_errandBoy', 'day', 'from_hour', 'to_hour', 'is_active', 'duration']
    search_fields = ['user', 'gofer_or_errandBoy', 'day', 'from_hour', 'to_hour']
    list_filter = ['created_at']


class BankAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipient_code', 'bank_name', 'account_number', 'created_at', 'updated_at']
    search_fields = ['user', 'recipient_code', 'bank_name', 'account_number']
    list_filter = ['created_at', 'updated_at']


class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_pin', 'balance', 'created_at']
    search_fields = ['user', 'transaction_pin', 'balance']
    list_filter = ['created_at']

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'amount', 'transaction_type', 'created_at']
    search_fields = ['wallet', 'amount', 'transaction_type']
    list_filter = ['created_at']

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(Hour, HourAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Schedule, ScheduleAdmin)
