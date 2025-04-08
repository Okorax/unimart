import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .tasks import resize_image

def rename(instance, filename):
    upload_to = f'profile_pics/{instance.username}/'
    ext = filename.split('.')[-1]
    return os.path.join(upload_to, f'{uuid4().hex}.{ext}')

class User(AbstractUser):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]
    email = models.EmailField(unique=True, max_length=254, help_text="Required. Must provide a valid email address.", verbose_name='email address')
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=False,  # Not allowing the field to be blank
    )
    phone_number = models.CharField(max_length=25, null=True)
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(blank=False, help_text="Required.", verbose_name="date of birth")
    hub = models.ForeignKey('hubs.Hub', on_delete=models.PROTECT, null=True, related_name='users')
    image = models.ImageField(
        default="profile_pics/default.jpg", 
        upload_to=rename
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        related_name='custom_user_group'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='custom_user_group'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'date_of_birth']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        resize_image.delay(self.image.path)

class UserSubscription(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('events', 'Events'),
        ('p2p', 'P2P'),
        ('freelance', 'Freelance'),
        ('blogs', 'Blogs'),
        ('communities', 'Communities'),
        ('all', 'All')
    ]
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    subscribed_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscribers")
    service_type = models.CharField(
        max_length=20,
        default="all",
        choices=SERVICE_TYPE_CHOICES,
        help_text="The type of service this category belongs to."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        unique_together = ('subscriber', 'subscribed_to')\
        
    def __str__(self):
        return f"{self.subscriber} subscribes to {self.subscribed_to}"

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message}"