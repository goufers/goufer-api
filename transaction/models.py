from django.db import models
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

    

   

    


