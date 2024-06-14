from django.db import models
from user.models import CustomUser
from django.utils import timezone
import bcrypt
from django.utils.translation import gettext_lazy as _


def generate_hour_choices():
    hours = []
    for hour in range(0, 24):
        time_str = f"{hour:02}:00"
        hours.append((time_str, time_str))
    return hours


class Wallet(models.Model):
    ''' Wallet and transaction models '''
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wallet')
    transaction_pin = models.CharField(max_length=4, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    # hash the transaction pin
    def set_transaction_pin(self, pin):
        self.transaction_pin = bcrypt.hashpw(pin.encode(), bcrypt.gensalt()).decode()

    def check_transaction_pin(self, pin):
        return bcrypt.checkpw(pin.encode(), self.transaction_pin.encode())
    
    def _str_(self):
        return f'{self.user.username} Wallet'


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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='transfer_recipient')
    recipient_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f'{self.bank_name} - {self.account_number} ({self.user.username})'


class Hour(models.Model):
    name = models.CharField(max_length=10, choices=generate_hour_choices(), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Day(models.Model):
    DAY_CHOICES = [
        ('Mon', 'Mon'),
        ('Tues', 'Tues'),
        ('Wed', 'Wed'),
        ('Thur', 'Thur'),
        ('Fri', 'Fri'),
        ('Sat', 'Sat'),
        ('Sun', 'Sun'),
    ]
    name = models.CharField(max_length=10, choices=DAY_CHOICES, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='schedules')
    gofer_or_errandBoy = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='active_schedules', blank=True, null=True)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    from_hour = models.ForeignKey(Hour, on_delete=models.CASCADE, related_name='from_hour')
    to_hour = models.ForeignKey(Hour, on_delete=models.CASCADE, related_name='to_hour')
    is_active = models.BooleanField(default=True)
    duration = models.IntegerField(_("Duration (optional)"), null=True, blank=True) # days for which the schedule is active. Active if null
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'gofer_or_errandBoy', 'day', 'from_hour', 'to_hour'], name='unique_schedule')
        ]
        ordering = ['day__created_at', 'from_hour__created_at']

    def __str__(self):
        return f"{self.user.username}'s availability on {self.day.name} from {self.from_hour.name} to {self.to_hour.name}"




