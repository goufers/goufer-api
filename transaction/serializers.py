from rest_framework import serializers
from .models import Wallet, Transaction, Bank

class WalletSerializer(serializers.ModelSerializer):
    """Users Wallet model serializer"""
    class Meta:
        model = Wallet
        fields = ['custom_user', 'transaction_pin', 'balance', 'created_at']

class TransactionSerializer(serializers.ModelSerializer):
    """Users Transaction model serializer"""
    class Meta:
        model = Transaction
        fields = ['wallet', 'amount', 'transaction_type', 'created_at']

class BankSerializer(serializers.ModelSerializer):
    """Users Bank model serializer"""
    class Meta:
        model = Bank
        fields = ['custom_user', 'recipient_code', 'bank_name', 'account_number', 'created_at', 'updated_at']


class FundWalletSerializer(serializers.Serializer):
    """User wallet serializer"""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class TransferFundsSerializer(serializers.Serializer):
    """Fund transfer serializer"""
    recipient = serializers.CharField(max_length=150)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

