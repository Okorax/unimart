from celery import shared_task
import datetime, pytz
from django.utils import timezone
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
from .models import Product
from utils.models import LastProcessed

@shared_task
def update_product_search_vectors():
    
    # Capture the current run to cut off for this run
    now = timezone.now()

    # Get or create the last processed last timestamp 
    last_processed, created = LastProcessed.objects.get_or_create(
        task_name="update_product_search_vectors",
        defaults={"last_timestamp": datetime.datetime.min.replace(tzinfo=pytz.utc)}
    )

    last_timestamp = last_processed.last_timestamp

    # Find records modified since the last run
    modified_products = Product.objects.filter(
        Q(updated_at__gt=last_timestamp)
    )

    if modified_products.exists():
        # Update search_vector in bulk using the database
        modified_products.update(search_vector=SearchVector('name', 'descriptions', 'status', 'price', 'condition', 'pickup_location'))
    
        # Compute meta_keywords and meta_description for each product
        for product in modified_products:
            product.meta_keywords = product.generate_meta_keywords()
            product.meta_description = product.generate_meta_description()
    
        # Perform bulk update for meta_keywords and meta_description
        Product.objects.bulk_update(modified_products, ['meta_keywords', 'meta_description'])
    
    last_processed.last_timestamp = now
    last_processed.save()