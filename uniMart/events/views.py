from django.shortcuts import render, get_object_or_404
from .models import Event
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.contrib.postgres.search import SearchQuery

# Create your views here.

def home(request):
    # Fetch events with attendee count
    events = Event.objects.all().select_related('organizer').annotate(attendee_count=Count('attendees'))
    # Get IDs of events the user is attending
    if request.user.is_authenticated:
        attending_event_ids = list(request.user.events_attending.values_list('id', flat=True))
    else:
        attending_event_ids = []
    return render(request, 'events/home.html', {
        'events': events,
        'attending_event_ids': attending_event_ids
    })

def detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, "events/event_detail.html", {"event": event})

def search(request):
    q = request.GET.get("events-search")
    events = Event.objects.filter(search_vector=SearchQuery(q))
    return render(request, "events/home.html", {"events": events})

@csrf_exempt
def attend_event(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    if request.method == "POST" and request.user.is_authenticated:
        # Add user to attendees (assuming a ManyToManyField named 'attendees')
        if request.user in event.attendees.all():
            event.attendees.remove(request.user)
        else:
            event.add_attendee(request.user)
    # Calculate updated attendee count
    attendee_count = event.attendees.count()
    # Check if user is attending
    is_attending = request.user.is_authenticated and request.user in event.attendees.all()
    # Render and return the updated footer
    return render(request, 'events/partials/event_footer.html', {
        'event': event,
        'attendee_count': attendee_count,
        'is_attending': is_attending
    })