import os
from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from utils.models import TimeStampedModel
from accounts.models import User
from django.utils.text import slugify

class Product(TimeStampedModel):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)]
    )
    hub = models.ForeignKey('hubs.Hub', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listed_products')
    category = models.ForeignKey('utils.Category', 
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        limit_choices_to={'service_type': 'p2p'},
        related_name='p2p')
    tags = models.ManyToManyField('utils.Tag', blank=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='good')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    views_count = models.PositiveIntegerField(default=0)  # Track product popularity
    pickup_location = models.CharField(max_length=200, blank=True)  # e.g., "Campus Library"
    search_vector = SearchVectorField(null=True, blank=True)
    slug = models.SlugField(max_length=100, blank=True)
    meta_keywords = models.CharField(null=True, blank=True, max_length=255, help_text='Comma delimited set of SEO keywords for meta tag')
    meta_description = models.CharField(null=True, blank=True, max_length=255, help_text='Content for description meta tag')


    class Meta:
        indexes = [models.Index(fields=['status', 'created_at'])]  # Optimize queries

    def __str__(self):
        return f"{self.name} ({self.get_condition_display()}) - {self.price}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.name} - Product")[:90]
            slug = base_slug
            jitter = uuid4().hex[:8]
            slug = f"{base_slug}-{jitter}"
            self.slug = slug
        super().save(*args, **kwargs)
    
    def generate_meta_description(self):
        """Generate a meta description based on available fields."""
        if self.description:
            return self.description[:150]  # Trim to 150 characters
        # Construct a sentence if description is missing
        category_str = f"a {self.category.name} " if self.category else ""
        return f"Buy {self.name}, {category_str} from {self.seller.username} at {self.pickup_location}."[:150]

    def generate_meta_keywords(self):
        """Generate a comma-separated list of keywords from related fields."""
        keywords = [self.name, self.pickup_location]
        if self.category:
            keywords.append(self.category.name)
        keywords.extend([self.hub.name, self.seller.username])
        return ", ".join(keywords)
    
    @property
    def thumbnail(self):
        default_thumbnail = self.images.filter(is_thumbnail=True).first()
        if default_thumbnail:
            return default_thumbnail
        default_thumbnail = self.images.first()
        default_thumbnail.is_thumbnail = True
        default_thumbnail.save()
        return default_thumbnail
    
def rename(instance, filename):
    upload_to = f'p2p/{instance.product.slug}/'
    ext = filename.split('.')[-1]
    return os.path.join(upload_to, f'{uuid4().hex}.{ext}')

class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=rename, default='p2p/default.png')
    is_thumbnail = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk and not ProductImage.objects.filter(product=self.product).exists():
            self.is_thumbnail = True

        if self.is_thumbnail:
            ProductImage.objects.filter(product=self.product).exclude(id=self.id).update(is_thumbnail=False)

        super().save(*args, **kwargs)

class PurchaseRequest(TimeStampedModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='requests')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buy_requests')
    offered_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)], 
        blank=True, 
        null=True
    )  # Allow negotiation
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('product', 'buyer')  # Prevent duplicate requests

    def __str__(self):
        return f"{self.buyer.username} -> {self.product.name} ({self.status})"
    
class Message(TimeStampedModel):
    purchase_request = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.sender.username} - message"

# Transaction model to track completed sales
class Transaction(TimeStampedModel):
    product = models.OneToOneField(Product, on_delete=models.PROTECT, related_name='transaction')
    purchase_request = models.OneToOneField(PurchaseRequest, on_delete=models.PROTECT, related_name='transaction')
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    completed_at = models.DateTimeField(default=timezone.now)
    buyer_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        null=True, 
        blank=True
    )  # 1-5 stars
    seller_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        null=True, 
        blank=True
    )
    buyer_feedback = models.TextField(max_length=500, blank=True)
    seller_feedback = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"Transaction: {self.product.name} sold for {self.final_price}"