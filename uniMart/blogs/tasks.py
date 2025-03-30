from celery import shared_task
import datetime, pytz
from django.utils import timezone
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
from .models import Post
from utils.models import LastProcessed

@shared_task
def update_post_search_vectors():
    
    # Capture the current run to cut off for this run
    now = timezone.now()

    # Get or create the last processed last timestamp 
    last_processed, created = LastProcessed.objects.get_or_create(
        task_name="update_post_search_vectors",
        defaults={"last_timestamp": datetime.datetime.min.replace(tzinfo=pytz.utc)}
    )

    last_timestamp = last_processed.last_timestamp

    # Find records modified since the last run
    modified_posts = Post.objects.filter(
        Q(updated_at__gt=last_timestamp)
    )

    if modified_posts.exists():
        # Update search_vector in bulk using the database
        modified_posts.update(search_vector=SearchVector('title', 'content'))
    
        # Compute meta_keywords and meta_description for each event
        for post in modified_posts:
            post.meta_keywords = post.generate_meta_keywords()
            post.meta_description = post.generate_meta_description()
    
        # Perform bulk update for meta_keywords and meta_description
        Post.objects.bulk_update(modified_posts, ['meta_keywords', 'meta_description'])
    
    last_processed.last_timestamp = now
    last_processed.save()