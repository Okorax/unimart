from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Post, PostImage

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1  # Number of empty forms to display

@admin.register(Post)
class EventAdmin(ModelAdmin):
    inlines = [PostImageInline]

@admin.register(PostImage)
class PostImageModel(ModelAdmin):
    pass