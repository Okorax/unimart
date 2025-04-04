from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Event, EventImage

# Register your models here.
class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1  # Number of empty forms to display

@admin.register(Event)
class EventAdmin(ModelAdmin):
    inlines = [EventImageInline]

admin.site.register(EventImage, ModelAdmin)