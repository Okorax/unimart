import os
from uuid import uuid4
from django.db import models
from django.utils.text import slugify
from accounts.models import User
from utils.models import TimeStampedModel
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

# Create your models here.

class Post(TimeStampedModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    hub = models.ForeignKey('hubs.Hub', on_delete=models.PROTECT, related_name='posts')
    category = models.ForeignKey('utils.Category', limit_choices_to={'service_type': 'blogs'}, on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField('utils.Tag', blank=True)
    slug = models.SlugField(blank=True, max_length=100)
    search_vector = SearchVectorField(null=True, blank=True)
    meta_keywords = models.CharField(null=True, blank=True, max_length=255, help_text='Comma delimited set of SEO keywords for meta tag')
    meta_description = models.CharField(null=True, blank=True, max_length=255, help_text='Content for description meta tag')

    class Meta:
        unique_together = [['hub', 'slug']]
        ordering = ['-created_at']
        indexes = [
            GinIndex(fields=['search_vector'], name='post_search_idx'),
        ]

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:90]
            slug = base_slug
            jitter = uuid4().hex[:8]
            slug = f"{base_slug}-{jitter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def generate_meta_description(self):
        """Generate a meta description based on available fields."""
        return self.content[:150]  # Trim to 150 characters

    def generate_meta_keywords(self):
        """Generate a comma-separated list of keywords from related fields."""
        keywords = [self.title]
        if self.category:
            keywords.append(self.category.name)
        keywords.extend([self.hub.name, self.author.username])
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
    upload_to = f'blogs/{instance.post.slug}/'
    ext = filename.split('.')[-1]
    return os.path.join(upload_to, f'{uuid4().hex}.{ext}')

class PostImage(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=rename, default='blogs/default.png')
    is_thumbnail = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk and not PostImage.objects.filter(post=self.post).exists():
            self.is_thumbnail = True

        if self.is_thumbnail:
            PostImage.objects.filter(post=self.post).exclude(id=self.id).update(is_thumbnail=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.post.title} image"