from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Hub

@admin.register(Hub)
class HubAdmin(ModelAdmin):
    pass