from django.contrib import admin
from .models import SubscriptionPlan, SubscriptionPlanItem, UserSubscription, PaymentTransaction

class SubscriptionPlanItemInline(admin.TabularInline):
    model = SubscriptionPlanItem
    extra = 1

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "duration_days", "is_active")
    inlines = [SubscriptionPlanItemInline]

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "start_date", "end_date", "is_active")

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_ref", "amount", "status", "created_at")