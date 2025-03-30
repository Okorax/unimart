from django.urls import path
from .views import home, attend_event, search, detail

urlpatterns = [
    path('', home, name="event-home"),
    path('search/results/', search, name="event-search"),
    path('attend/<slug:event_slug>/', attend_event, name='attend_event'),
    path('detail/<slug:slug>/', detail, name="event-detail")
]