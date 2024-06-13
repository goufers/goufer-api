from rest_framework import serializers
from .models import Wallet, Transaction, Bank, Hour, Day, Schedule

class WalletSerializer(serializers.ModelSerializer):
    """Users Wallet model serializer"""
    class Meta:
        model = Wallet
        fields = ['user', 'transaction_pin', 'balance', 'created_at']

class TransactionSerializer(serializers.ModelSerializer):
    """Users Transaction model serializer"""
    class Meta:
        model = Transaction
        fields = ['wallet', 'amount', 'transaction_type', 'created_at']

class BankSerializer(serializers.ModelSerializer):
    """Users Bank model serializer"""
    class Meta:
        model = Bank
        fields = ['user', 'recipient_code', 'bank_name', 'account_number', 'created_at', 'updated_at']


class FundWalletSerializer(serializers.Serializer):
    """User wallet serializer"""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class TransferFundsSerializer(serializers.Serializer):
    """Fund transfer serializer"""
    recipient = serializers.CharField(max_length=150)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class HourSerializer(serializers.ModelSerializer):
    """Hours model serializer"""
    class Meta:
        model = Hour
        fields = ['id', 'name', 'created_at']


class DaySerializer(serializers.ModelSerializer):
    """Day model serializer"""
    class Meta:
        model = Day
        fields = ['id', 'name', 'created_at']


class ScheduleSerializer(serializers.ModelSerializer):
    """Schedule model serializer"""
    user = serializers.StringRelatedField()
    gofer_or_errandBoy = serializers.StringRelatedField()

    class Meta:
        model = Schedule
        fields = ['id', 'user', 'gofer_or_errandBoy', 'day', 'from_hour', 'to_hour', 'is_active', 'duration']
