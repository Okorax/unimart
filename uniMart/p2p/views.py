from django.shortcuts import render
from .models import Product
from django.views.decorators.csrf import csrf_exempt
from django.contrib.postgres.search import SearchQuery

def home(request):
    products = Product.objects.all()
    return render(request, "p2p/home.html", context={"products": products})

@csrf_exempt
def make_request(request, product_slug):
    return render(request, "p2p/partials/make_request.html")

def search(request):
    q = request.GET.get("products-search")
    products = Product.objects.filter(search_vector=SearchQuery(q))
    return render(request, "p2p/home.html", {"products": products})
