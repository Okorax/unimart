from django.shortcuts import render, get_object_or_404
from .models import Event
from django.db.models import Count, Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.postgres.search import SearchQuery

def home(request):
    category_slug = request.GET.get("category")

    # Base queryset with common optimizations
    events = Event.objects.all().select_related('organizer').annotate(attendee_count=Count('attendees'))
    
    # Apply filter only if category is provided
    if category_slug:
        events = events.filter(category__slug=category_slug)

    # Get attending event IDs if user is authenticated
    attending_event_ids = (
        list(request.user.events_attending.values_list('id', flat=True))
        if request.user.is_authenticated
        else []
    )

    return render(request, 'events/home.html', {
        'events': events[:40],
        'attending_event_ids': attending_event_ids
    })

def detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, "events/event_detail.html", {"event": event})

def search(request):
    q = request.GET.get("events-search").split()
    template = "events/home.html"
    if q:
        search_terms = [f"{search_term}:*" for search_term in q if search_term.strip()]
        search_query = " & ".join(search_terms) if search_terms else "''"
        events = Event.objects.filter(search_vector=SearchQuery(search_query, search_type="raw"))
        return render(request, template, {"events": events[:40]})
    return render(request, template, {"events": Event.objects.none()})

def get_user_event(request, user_slug):
    events = get_object_or_404(Event, user=request.user)
    return render(request, "events/home.html", {"events", events})

def get_user_subscribed_events(request):
    template = "events/home.html"
    if request.user.is_authenticated:
        events = Event.objects.none()
        return render(request, template, {"events": events})
    subscriptions = request.user.subscriptions.filter(Q(service_type="events") | Q(service_type="all"))
    organizers = [sub.subscribed_to for sub in subscriptions]
    events = Event.objects.filter(organizer__in=organizers)
    return render(request, template, {"events": events})

    

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