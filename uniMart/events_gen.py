import json
import random
from datetime import datetime, timedelta
from django.utils.text import slugify
import pytz
import uuid

# Use Africa/Lagos timezone
TIMEZONE = pytz.timezone("Africa/Lagos")

# Data pools
EVENT_TYPES = [
    "Tech Summit", "Career Fair", "Cultural Festival", "Hackathon", "Workshop",
    "Seminar", "Concert", "Sports Day", "Charity Run", "Art Exhibition",
    "Science Fair", "Networking Event", "Food Festival", "Health Awareness",
    "Entrepreneurship Bootcamp"
]

YEARS = [2025, 2026]
LOCATIONS = ["Owerri", "FUTO", "Ihiagwa", "New Owerri", "Eziobodo"]

ADDRESSES = [
    "FUTO Main Campus, Ihiagwa, Owerri, Imo State",
    "Ihiagwa Road, Opposite FUTO Gate, Owerri",
    "Umuchima Village, Near FUTO, Ihiagwa",
    "Obinze Road, 5km from FUTO, Owerri",
    "Eziobodo Community, Near FUTO, Owerri",
    "World Bank Housing Estate, New Owerri",
    "Wetheral Road, Owerri City Center",
    "Okigwe Road, Near Owerri Main Market",
    "Douglas Road, Owerri Central",
    "Naze Junction, 10km from FUTO, Owerri",
    "Orlu Road, Amakohia, Owerri",
    "Control Post, Mbieri Road, Owerri",
    "Umuguma Housing Estate, New Owerri",
    "Aladinma Estate, Owerri",
    "Works Layout, Owerri"
]

DESCRIPTIONS = [
    "A summit showcasing the latest trends and innovations.",
    "Celebrate with music, dance, and local traditions.",
    "Code your way to victory in this exciting challenge.",
    "Learn from experts in an interactive session.",
    "A fun-filled day for all participants."
]

def random_datetime(year):
    start = datetime(year, 4, 10, tzinfo=TIMEZONE)
    end = datetime(year, 12, 31, tzinfo=TIMEZONE)
    delta = end - start
    random_days = random.randrange(delta.days)
    base_date = start + timedelta(days=random_days)
    start_time = base_date.replace(hour=random.randint(8, 18), minute=0, second=0)
    duration = random.randint(1, 8)
    end_time = start_time + timedelta(hours=duration)
    return start_time.isoformat(), end_time.isoformat()

# Generate 5000 unique events
events = []
used_names = set()

for i in range(5000):
    year = random.choice(YEARS)
    event_type = random.choice(EVENT_TYPES)
    location = random.choice(LOCATIONS)
    name = f"{event_type} {year} {location}"
    
    while name in used_names:
        name = f"{event_type} {year} {location} {i + 1}"
    used_names.add(name)
    
    start_time, end_time = random_datetime(year)
    slug = slugify(f"{name}-{start_time[:10]}-{uuid.uuid4().hex[:8]}")[:100]
    
    now = TIMEZONE.localize(datetime(2025, 4, 9, 10, 0))
    start_dt = datetime.fromisoformat(start_time)
    end_dt = datetime.fromisoformat(end_time)
    if start_dt > now:
        status = "planned"
    elif start_dt <= now < end_dt:
        status = "ongoing"
    else:
        status = "completed"

    event = {
        "model": "events.Event",
        "pk": i + 1,
        "fields": {
            "hub": 1,
            "name": name,
            "organizer": random.choice([1, 2]),
            "attendees": [],
            "start_time": start_time,
            "end_time": end_time,
            "venue": random.choice(ADDRESSES),
            "capacity": random.randint(50, 5000),
            "category": random.randint(1, 7),  # Random category ID from 1 to 7
            #"search_vector": None,
            "slug": slug,
            "status": status,
            "description": random.choice(DESCRIPTIONS),
            "meta_keywords": f"{name}, {location}, FUTO",
            "meta_description": f"{name} at {random.choice(ADDRESSES)} on {start_time[:10]}.",
            "created_at": TIMEZONE.localize(datetime.now()).isoformat(),
            "updated_at": TIMEZONE.localize(datetime.now()).isoformat()
        }
    }
    events.append(event)

# Save to file
with open("event_fixtures.json", "w") as f:
    json.dump(events, f, indent=2)

print("Generated 5000 unique events with categories in 'event_fixtures.json'.")