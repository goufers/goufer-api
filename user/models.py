from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg
from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver



MOBILILTY_CHOICES = [
    ('Bicycle', 'Bicycle'),
    ('Motorcycle', 'Motorcycle'),
    ('Car', 'Car'),
    ('Truck', 'Truck'),
    ('Van', 'Van'),
    ('Bus', 'Bus'),
    ('Other', 'Other')
]

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Others')
]

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True "
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True"
            )

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Base user class for authentication"""
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    phone_number = models.CharField(max_length=30, unique=True, db_index=True)
    profile_picture = models.ImageField(upload_to='files/dp', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    location = models.ForeignKey("main.Location", on_delete=models.CASCADE, blank=True, null=True)
    address = models.ForeignKey("main.Address", on_delete=models.CASCADE, blank=True, null=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='user_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='user_user_permissions')
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()
    
    def __str__(self) -> str:
        return self.email
    
    # def save(self, *args, **kwargs):
    #     if not self.address:
    #         Address = apps.get_model('main', 'Address')
    #         self.address = Address.objects.create()  # Create a default Address
    #     super().save(*args, **kwargs)
        
@receiver(post_save, sender=CustomUser)
def create_default_address(sender, instance, created, **kwargs):
    if created and not instance.address:
        Address = apps.get_model('main', 'Address')
        instance.address = Address.objects.create()
        instance.save()


class Gofer(models.Model):
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='gofer')
    expertise = models.CharField(max_length=200, default=None, db_index=True)
    mobility_means = models.CharField(max_length=20, choices=MOBILILTY_CHOICES, default='Motorcycle', db_index=True)
    bio = models.TextField(max_length=1024)
    sub_category = models.ForeignKey('main.SubCategory', on_delete=models.PROTECT, related_name='gofers', default=None)
    charges = models.IntegerField(default=0)
    is_available  = models.BooleanField(default=True)
    avg_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    
    def __str__(self) -> str:
        return f"Gofer {self.custom_user.email}"
    
    def update_rating(self):
        reviews = self.gofer_reviews.all()
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        self.avg_rating = average_rating or 0.00
        self.save()

    def toggle_availability(self):
        return not self.is_available
    
class Vendor(models.Model):
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='vendor')
    business_name = models.CharField(max_length=255)
    category = models.OneToOneField('main.Category', on_delete=models.CASCADE, related_name='vendor_category')
    website = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    # SOCIAL LINKS
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    def __str__(self):
        return self.business_name

class Media(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_media')
    media = models.ImageField(upload_to='media/vendors/media')
    
    def __str__(self) -> str:
        return self.gofer.custom_user.email
    
    
class Availability(models.Model):
    """ Defines times of gofer or entertainer availability """
    gofer = models.ForeignKey(Gofer, on_delete=models.CASCADE, related_name='availability')
    start_time = models.TimeField()
    end_time = models.TimeField()
    days_of_week = models.JSONField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.gofer.user.username} - {self.start_time} - {self.end_time}'
    
class Errand(models.Model):
    """Associates a gofer to a user task"""
    ERRAND_STATUS = [
    ("Completed", "Completed"),
    ("Ongoing", "Ongoing"),
    ("Terminated", "Terminated")
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='errands_sent')
    task_description = models.TextField()
    sub_category = models.ForeignKey('main.SubCategory', on_delete=models.CASCADE)
    gofer = models.ForeignKey(Gofer, on_delete=models.CASCADE, related_name='errands')
    estimated_duration = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=ERRAND_STATUS, default="O")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.gofer.username}'
    

class ErrandBoy(models.Model):
    """An errand messanger for user task"""
    MOBILILTY_CHOICES = [
    ('Bicycle', 'Bicycle'),
    ('Motorcycle', 'Motorcycle'),
    ('Car', 'Car'),
    ('Truck', 'Truck'),
    ('Van', 'Van'),
    ('Bus', 'Bus'),
    ('Other', 'Other')
]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="errand_boy")
    mobility_means = models.CharField(max_length=20, choices=MOBILILTY_CHOICES, default='Bicycle')
    charges = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"Errandboy {self.user.first_name}"




class ProGofer(models.Model):
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='pro_gofer')
    bio = models.TextField(blank=True, null=True)
    profession = models.CharField(max_length=255)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.custom_user.first_name} - {self.profession}'
    
    
    
class MessagePoster(models.Model):
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='message_poster')

    def __str__(self) -> str:
        return self.custom_user.first_name
    
    
    
class Schedule(models.Model):

    DAY_CHOICES = [
        ('mon', 'Monday'),
        ('tues', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thur', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    ]

    pro_gofer = models.ForeignKey(ProGofer, on_delete=models.CASCADE, related_name='schedules')
    day_of_week_available = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time_available = models.TimeField()
    end_time_available = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.pro_gofer.custom_user.first_name} is available on {self.day} from {self.start_time_available} to {self.end_time_available}"
    
class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    )
    
    scheduled_date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    purpose = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message_poster = models.ForeignKey(MessagePoster, on_delete=models.CASCADE, related_name='bookings_created')
    pro_gofer = models.ForeignKey(ProGofer, on_delete=models.CASCADE, related_name='bookings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.message_poster.custom_user.first_name} booked {self.pro_gofer.custom_user.first_name} on {self.scheduled_day} from {self.schedule.from_time} to {self.schedule.to_time}"

    