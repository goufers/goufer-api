from rest_framework import serializers
from .models import Wallet, Transaction, Bank, Schedule, Booking

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





class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'gofer', 'day', 'from_hour', 'to_hour', 'duration', 'created_at', 'updated_at']


    def create(self, validated_data):
        return Schedule.objects.create(**validated_data)


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'message_poster', 'pro_gofer', 'schedule', 'duration', 'is_active', 'status', 'comment', 'booked_at', 'updated_at']
        read_only_fields = ['status', 'comment', 'booked_at', 'updated_at']

    def create(self, validated_data):
        message_poster = validated_data['message_poster']
        pro_gofer = validated_data['pro_gofer']
        schedule = validated_data['schedule']
        duration = validated_data['duration']
        total_cost = pro_gofer.hourly_rate * duration

        if message_poster.wallet.balance >= total_cost:
            message_poster.wallet.balance -= total_cost
            message_poster.wallet.save()
            return super().create(validated_data)
        else:
            raise serializers.ValidationError("Insufficient balance.")