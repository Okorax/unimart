from django.urls import path
from .views import home, make_request, search

urlpatterns = [
    path('', home, name="p2p-home"),
    path('make_request/<slug:product_slug>/', make_request, name="make_request"),
    path('search/results/', search, name="product-search")
]