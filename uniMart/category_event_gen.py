import json
from django.utils.text import slugify
from datetime import datetime
import pytz

# Use Africa/Lagos timezone (Nigeria)
TIMEZONE = pytz.timezone("Africa/Lagos")

# Define event categories
EVENT_CATEGORIES = [
    {"name": "Technology", "description": "Events focused on tech and innovation."},
    {"name": "Culture", "description": "Cultural celebrations and festivals."},
    {"name": "Sports", "description": "Sporting events and competitions."},
    {"name": "Education", "description": "Workshops, seminars, and learning sessions."},
    {"name": "Health", "description": "Health awareness and wellness events."},
    {"name": "Business", "description": "Networking and entrepreneurship events."},
    {"name": "Arts", "description": "Art exhibitions, concerts, and performances."},
]

# Generate category fixture
categories = []
for i, cat in enumerate(EVENT_CATEGORIES, start=1):
    category = {
        "model": "utils.Category",  # Adjust app name as needed (e.g., "utils")
        "pk": i,
        "fields": {
            "name": cat["name"],
            "hub": 1,  # Tied to Hub ID 1
            "service_type": "events",
            "slug": slugify(cat["name"]),
            "description": cat["description"],
            "meta_keywords": f"{cat['name']}, events, FUTO, Owerri",
            "meta_description": f"{cat['name']} events at FUTO and Owerri.",
            "created_at": TIMEZONE.localize(datetime.now()).isoformat(),
            "updated_at": TIMEZONE.localize(datetime.now()).isoformat()
        }
    }
    categories.append(category)

# Save to file
with open("category_fixtures.json", "w") as f:
    json.dump(categories, f, indent=2)

print("Generated category fixture in 'category_fixtures.json'.")