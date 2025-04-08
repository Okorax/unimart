from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver
from .models import Event, EventImage
from accounts.models import UserSubscription, Notification

@receiver(post_save, sender=Event)
def create_event_image(sender, instance, created, **kwargs):
    if created:
        EventImage.objects.create(event=instance)
        organizer = instance.organizer
        subscribers = UserSubscription.objects.filter(Q(subscribed_to=organizer) & (Q(service_type="events") | Q(service_type="all")))
        notifications = [
            Notification(
                recipient=sub.subscriber,
                sender=organizer,
                message=f"{organizer.username} created a new event: {instance.name}"
            )
            for sub in subscribers
        ]
        Notification.objects.bulk_create(notifications)
