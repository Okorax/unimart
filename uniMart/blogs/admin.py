from django.contrib import admin
from .models import Post, PostImage

# Register your models here.

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1  # Number of empty forms to display

@admin.register(Post)
class EventAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]

admin.site.register(PostImage)