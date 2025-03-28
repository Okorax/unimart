from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event, EventImage

@receiver(post_save, sender=Event)
def create_event_image(sender, instance, created, **kwargs):
    if created:
        EventImage.objects.create(event=instance)