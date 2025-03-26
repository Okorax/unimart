from celery import shared_task
import datetime, pytz
from django.utils import timezone
from django.core.management import call_command
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
from .models import Event
from utils.models import LastProcessed

@shared_task
def update_event_statuses():
    call_command('update_event_statuses')

@shared_task
def update_event_search_vectors():
    
    # Capture the current run to cut off for this run
    now = timezone.now()

    # Get or create the last processed last timestamp 
    last_processed, created = LastProcessed.objects.get_or_create(
        task_name="update_event_search_vectors",
        defaults={"last_timestamp": datetime.datetime.min.replace(tzinfo=pytz.utc)}
    )

    last_timestamp = last_processed.last_timestamp

    # Find records modified since the last run
    modified_events = Event.objects.filter(
        Q(updated_at__gt=last_timestamp)
    )

    if modified_events.exists():
        # Update search_vector in bulk using the database
        modified_events.update(search_vector=SearchVector('name', 'venue', 'description'))
    
        # Compute meta_keywords and meta_description for each event
        for event in modified_events:
            event.meta_keywords = event.generate_meta_keywords()
            event.meta_description = event.generate_meta_description()
    
        # Perform bulk update for meta_keywords and meta_description
        Event.objects.bulk_update(modified_events, ['meta_keywords', 'meta_description'])
    
    last_processed.last_timestamp = now
    last_processed.save()