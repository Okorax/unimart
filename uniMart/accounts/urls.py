from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from .views import UserCreateView, UserLoginView
from django.contrib.auth import views as auth_views

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path('login/', UserLoginView.as_view(), name="accounts-login"),
    path('register/', UserCreateView.as_view(), name="accounts-register"),
    path('logout/', auth_views.LogoutView.as_view(), name='accounts-logout'),
    path('sitemap.xml', sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap")
]