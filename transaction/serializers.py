from rest_framework import serializers
from .models import Wallet, Transaction, Bank, Schedule, Booking, ProGofer, MessagePoster
from django.shortcuts import get_object_or_404

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
    pro_gofer = serializers.PrimaryKeyRelatedField(queryset=ProGofer.objects.all(), required=True)

    class Meta:
        model = Schedule
        fields = ['id', 'pro_gofer', 'day', 'from_hour', 'to_hour', "maximum_bookings", 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """
        Check that the from_hour is before the to_hour.
        """
        if data['from_hour'] >= data['to_hour']:
            raise serializers.ValidationError("from_hour must be before to_hour")
        
        # Check for schedule conflicts
        if Schedule.objects.filter(
            pro_gofer=data['pro_gofer'],
            day=data['day'],
            from_hour=data['from_hour'],
            to_hour=data['to_hour']
        ).exists():
            raise serializers.ValidationError("A schedule with the same time already exists for this user.")
        
        return data

    # You can override the create method if you need additional logic
    def create(self, validated_data):
        return Schedule.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.day = validated_data.get('day', instance.day)
        instance.from_hour = validated_data.get('from_hour', instance.from_hour)
        instance.to_hour = validated_data.get('to_hour', instance.to_hour)
        instance.save()
        return instance


class BookingSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer()
    
    class Meta:
        model = Booking
        fields = ['id', 'message_poster', 'pro_gofer', 'schedule', 'duration', 'is_active', 'status', 'comment', 'booked_at', 'updated_at']
        read_only_fields = ['status', 'comment', 'booked_at', 'updated_at']

    def create(self, validated_data):
        self.update_booking_count(validated_data)
        return super().create(validated_data)

    def update_booking_count(self, validated_data):
        duration = validated_data['duration']
        pro_gofer = validated_data['pro_gofer']
        total_cost = pro_gofer.hourly_rate * duration
        user_wallet = get_object_or_404(Wallet, custom_user=pro_gofer.custom_user)

        if user_wallet.balance >= total_cost:
            user_wallet.balance -= total_cost
            user_wallet.save()
            pro_gofer.maximum_bookings += 1
            pro_gofer.save()
        else:
            raise serializers.ValidationError("Insufficient balance.")
