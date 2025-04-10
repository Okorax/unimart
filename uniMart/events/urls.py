from django.urls import path
from .views import home, attend_event, search, detail, get_user_subscribed_events

urlpatterns = [
    path('', home, name="event-home"),
    path('search/results/', search, name="event-search"),
    path('my-events/', get_user_subscribed_events, name='my_event'),
    path('attend/<slug:event_slug>/', attend_event, name='attend_event'),
    path('detail/<slug:slug>/', detail, name="event-detail")
]