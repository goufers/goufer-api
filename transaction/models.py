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


class ContractManager(models.Manager):
    """Contract manager class"""
    def create_contract(self, user, gofer_or_errandBoy, contract_length, start_date, end_date, pay_rate):
        contract = self.create(
            user=user,
            gofer_or_errandBoy=gofer_or_errandBoy,
            contract_length=contract_length,
            start_date=start_date,
            end_date=end_date,
            pay_rate=pay_rate,
        )
        return contract

    def get_contracts(self, user):
        """Get all contracts for a user"""
        return self.filter(user=user)
    
    def get_contract(self, user, contract_code):
        """Get a contract by code"""
        return self.get(user=user, contract_code=contract_code)
    
    def get_active_contracts(self, user):
        """Get all active contracts for a user"""
        return self.filter(user=user, contract_status='Active')
    
    def get_pending_contracts(self, user):
        """Get all pending contracts for a user"""
        return self.filter(user=user, contract_status='Pending')
    
    def get_settled_contracts(self, user):
        """Get all settled contracts for a user"""
        return self.filter(user=user, contract_status='Settled')
    
    def get_declined_contracts(self, user):
        """Get all declined contracts for a user"""
        return self.filter(user=user, contract_status='Declined')
    
    def get_terminated_contracts(self, user):
        """Get all terminated contracts for a user"""
        return self.filter(user=user, contract_status='Terminated')
    
    def get_contract_by_code(self, contract_code):
        return self.get(contract_code=contract_code)
    


class Contract(models.Model):
    """Contract model"""
    CONTRACT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Active', 'Active'),
        ('Settled', 'Settled'),
        ('Declined', 'Declined'),
        ('Terminated', 'Terminated'),
    ]
    contract_code = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(CustomUser, related_name='contracts', on_delete=models.CASCADE)
    gofer_or_errandBoy = models.ForeignKey(CustomUser, related_name = 'contract', on_delete=models.CASCADE)
    contract_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_rate = models.DecimalField(max_digits=10, decimal_places=2) # per day or per hour
    contract_length = models.IntegerField() # this is duration in days
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    days_remaining = models.IntegerField(default=0)
    contract_status = models.CharField(max_length=20, choices=CONTRACT_STATUS_CHOICES, default='Pending')
    remark = models.TextField(blank=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ContractManager()

    def __str__(self):
        return f"Contract #{self.pk} - {self.user} - {self.gofer_or_errandBoy} - {self.contract_length} days - {self.contract_status}"

    def save(self, *args, **kwargs):
        self.contract_amount = self.pay_rate * self.contract_length
        self.payment_remaining = max(self.contract_amount - self.payment_made, 0)
        self.days_remaining = max((self.end_date - timezone.now().date()).days, 0)
        if self.days_remaining == 0:
            self.contract_status = 'Settled'
        super().save(*args, **kwargs)
