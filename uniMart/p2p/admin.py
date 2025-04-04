from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Product, ProductImage

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    pass

@admin.register(ProductImage)
class ProductImageAdmin(ModelAdmin):
    pass