from django.db import models
from django.core.exceptions import ValidationError
from user.models import CustomUser, ProGofer
from main.models import MessagePoster
import bcrypt
from django.utils.translation import gettext_lazy as _


class Wallet(models.Model):
    ''' Wallet and transaction models '''
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wallet')
    transaction_pin = models.CharField(max_length=4, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    # hash the transaction pin
    def set_transaction_pin(self, pin):
        self.transaction_pin = bcrypt.hashpw(pin.encode(), bcrypt.gensalt()).decode()

    def check_transaction_pin(self, pin):
        return bcrypt.checkpw(pin.encode(), self.transaction_pin.encode())
    
    def _str_(self):
        return f'{self.custom_user.username} Wallet'


class Transaction(models.Model):
    """Users Transaction model"""
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions", default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal'), ('transfer', 'Transfer')])
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.transaction_type} - {self.amount} - {self.updated_at}"
    
    
class Bank(models.Model):
    """Users Bank information for withdrawals"""
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='transfer_recipient')
    recipient_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f'{self.bank_name} - {self.account_number} ({self.custom_user.username})'



def generate_hour_choices():
    hours = []
    for hour in range(0, 24):
        time_str = f"{hour:02}:00"
        hours.append((time_str, time_str))
    return hours


class Schedule(models.Model):
    """Professional users schedules"""
    DAY_CHOICES = [
        ('Mon', 'Monday'),
        ('Tues', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thur', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]

    pro_gofer = models.ForeignKey(ProGofer, on_delete=models.CASCADE, related_name='schedule')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    from_hour = models.CharField(max_length=10, choices=generate_hour_choices())
    to_hour = models.CharField(max_length=10, choices=generate_hour_choices())
    maximum_bookings = models.IntegerField(null=True, blank=True, default=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['day', '-created_at']
        constraints = [
            models.UniqueConstraint(fields=[ 'pro_gofer', 'day', 'from_hour', 'to_hour'], name='unique_schedule')
        ]

    def clean(self):
        super().clean()
        if Schedule.objects.filter(pro_gofer=self.pro_gofer, day=self.day, from_hour=self.from_hour, to_hour=self.to_hour).exists():
            raise ValidationError("This schedule already exists for the professional user.")
    def __str__(self):
        return f"{self.pro_gofer.custom_user.first_name} available on {self.day} from {self.from_hour} to {self.to_hour}"


class Booking(models.Model):
    """User-Professional booking"""
    BOOKING_CHOICES = [
        ('Active', 'Active'), 
        ('Terminated', 'Terminated'), # Only active booking
        ('Settled', 'Settled'), 
        ('Pending Approval', 'Pending Approval'),
        ('Declined', 'Declined'),
        ('Cancelled', 'Cancelled'), # A user can cancel
        ]
    message_poster = models.ForeignKey(MessagePoster, on_delete=models.CASCADE, related_name='bookings')
    pro_gofer = models.ForeignKey(ProGofer, on_delete=models.CASCADE, related_name='bookings')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='bookings')
    duration = models.PositiveSmallIntegerField(_('How long in hours?'), default=1)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=BOOKING_CHOICES, default='Pending Approval')
    comment = models.TextField(blank=True, null=True)  # For pro_gofer's comment on decline
    booked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.message_poster.custom_user.first_name} booked {self.pro_gofer.custom_user.first_name} on {self.schedule.day} from {self.schedule.from_hour} to {self.schedule.to_hour}"
