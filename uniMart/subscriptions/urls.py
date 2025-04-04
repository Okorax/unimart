from django.urls import path
from .views import subscribe

urlpatterns = [
    #path('', home, name="subscriptions-plans"),
    path("subscribe/<int:plan_id>/", subscribe, name='subscriptions-subscribe')
]