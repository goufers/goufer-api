from django.db import models
from .validate import validate_file_size
from user.models import CustomUser, Gofer
from django.core.validators import FileExtensionValidator


class Location(models.Model):
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return f"Gofer at {self.latitude}, {self.longitude}"

class Category(models.Model):
    CATEGORY_CHOICES = (
    ('food', 'Food'),
    ('entertainment', 'Entertainment'),
    ('transportation', 'Transportation'),
    ('tourism_and_travel', 'Tourism & Travel'),
    ('religious_donations', 'Religious Donations'),
    ('medical', 'Medical'),
    ('services', 'Services'),
    ('legal', 'Legal'), 
    ('technical', 'Technical'),
    ('employments', 'Employment'),
    ('housing', 'Housing'),
    ('shopping', 'Shopping'),
)
    category_name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Document(models.Model):
    
    DOCUMENT_CHOICES = (
        ('ssn', 'SSN'),
        ('nin', 'NIN')
    )
    
    document_type = models.CharField(max_length=5, choices=DOCUMENT_CHOICES)
    document_number = models.CharField(max_length=11)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="documents" )
    document_of_expertise = models.FileField(upload_to='main/documents', validators=[validate_file_size, FileExtensionValidator(allowed_extensions=['jpg', 'png', 'pdf'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.document_type
    
class Reviews(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_reviews')
    gofer = models.ForeignKey(Gofer, on_delete=models.CASCADE, related_name='gofer_reviews')
    comment = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now_add=True)
    
    
    
class Contract(models.Model):
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
    start_date = models.DateField()
    end_date = models.DateField()
    days_remaining = models.IntegerField(default=0)
    contract_status = models.CharField(max_length=20, choices=CONTRACT_STATUS_CHOICES, default='Pending')
    remark = models.TextField(blank=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"Contract #{self.pk} - {self.user} - {self.gofer_or_errandBoy} - {self.contract_length} days - {self.contract_status}"

    def save(self, *args, **kwargs):
        self.contract_amount = self.pay_rate * self.contract_length
        self.payment_remaining = max(self.contract_amount - self.payment_made, 0)
        self.days_remaining = max((self.end_date - timezone.now().date()).days, 0)
        if self.days_remaining == 0:
            self.contract_status = 'Settled'
        super().save(*args, **kwargs)
    

 