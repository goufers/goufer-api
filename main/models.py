from django.db import models
from .validate import validate_file_size
from user.models import Gofer, CustomUser, MessagePoster, ProGofer
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



class Location(models.Model):
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    def __str__(self) -> str:
        return f"Gofer at {self.latitude}, {self.longitude}"
    
class Address(models.Model):
    house_number = models.CharField(max_length=10, default="Number")
    street = models.CharField(max_length=255, default="Street name")
    city = models.CharField(max_length=255, default="City")
    state = models.CharField(max_length=50, default="State")
    country = models.CharField(max_length=50, default="Country")

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
    ('real_estate', 'Real Estate'),
)
    category_name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    
class Document(models.Model):
    DOCUMENT_CHOICES = (
        ('ssn', 'SSN'),
        ('nin', 'NIN')
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField(max_length=5, choices=DOCUMENT_CHOICES)
    document_number = models.CharField(max_length=11, unique=True)
    document_of_expertise = models.FileField(upload_to='main/documents', validators=[validate_file_size, FileExtensionValidator(allowed_extensions=['jpg', 'png', 'pdf'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    
    def __str__(self) -> str:
        return self.document_type


    
class Reviews(models.Model):
    message_poster = models.ForeignKey(MessagePoster, on_delete=models.CASCADE, related_name='user_reviews')
    gofer = models.ForeignKey(Gofer, on_delete=models.CASCADE, related_name='gofer_reviews')
    comment = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now_add=True)
    
@receiver(post_save, sender=Reviews)
@receiver(post_delete, sender=Reviews)
def update_gofer_rating(sender, instance, **kwargs):
    instance.gofer.update_rating()
    
    def __str__(self) -> str:
        return f"This is the review of {self.reviews.gofer}"
    
    


