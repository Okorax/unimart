from django.urls import path
from .views import home, attend_event, search

urlpatterns = [
    path('', home, name="event-home"),
    path('events/search/results/', search, name="event-search"),
    path('attend/<int:event_id>/', attend_event, name='attend_event'),
]