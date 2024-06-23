from rest_framework import serializers
from .models import Wallet, Transaction, Bank, Schedule, ProGofer, Booking

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





class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'gofer', 'day', 'from_hour', 'to_hour', 'duration', 'created_at', 'updated_at']


    def create(self, validated_data):
        return Schedule.objects.create(**validated_data)


class ProGoferSerializer(serializers.ModelSerializer):
    """Pro-gofer model serializer"""
    class Meta:
        model = ProGofer
        fields = ['user', 'profession', 'bio', 'hourly_rate', 'is_verified', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'gofer', 'schedule', 'duration', 'is_active', 'status', 'comment', 'booked_at', 'updated_at']
        read_only_fields = ['status', 'comment', 'booked_at', 'updated_at']

    def create(self, validated_data):
        user = validated_data['user']
        gofer = validated_data['gofer']
        schedule = validated_data['schedule']
        duration = validated_data['duration']
        total_cost = gofer.hourly_rate * duration

        if user.wallet.balance >= total_cost:
            user.wallet.balance -= total_cost
            user.wallet.save()
            return super().create(validated_data)
        else:
            raise serializers.ValidationError("Insufficient balance.")