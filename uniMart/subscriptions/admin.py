from unfold.admin import ModelAdmin, TabularInline
from django.contrib import admin
from .models import SubscriptionPlan, SubscriptionPlanItem, Subscription, PaymentTransaction

class SubscriptionPlanItemInline(TabularInline):
    model = SubscriptionPlanItem
    extra = 1

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(ModelAdmin):
    list_display = ("name", "price", "duration_days", "is_active")
    inlines = [SubscriptionPlanItemInline]

@admin.register(Subscription)
class UserSubscriptionAdmin(ModelAdmin):
    list_display = ("user", "plan", "start_date", "end_date", "is_active")

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(ModelAdmin):
    list_display = ("transaction_ref", "amount", "status", "created_at")