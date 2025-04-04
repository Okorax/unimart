from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import SearchHistory, Tag, Category, About, Client, LastProcessed#, Brand

@admin.register(Tag)
class TagAdmin(ModelAdmin):
    pass

#admin.site.register(Brand)
@admin.register(Client)
class ClienAdmin(ModelAdmin):
    pass

@admin.register(About)
class AboutAdmin(ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    pass

@admin.register(LastProcessed)
class LastProcessedAdmin(ModelAdmin):
    pass

@admin.register(SearchHistory)
class SearchHistoryAdmin(ModelAdmin):
    pass