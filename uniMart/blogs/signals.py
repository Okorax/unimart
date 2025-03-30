from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, PostImage

@receiver(post_save, sender=Post)
def create_event_image(sender, instance, created, **kwargs):
    if created:
        PostImage.objects.create(post=instance)