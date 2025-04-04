from django.db import models
from accounts.models import User
from django.utils import timezone

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ₦{self.price}"

class SubscriptionPlanItem(models.Model):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name="items")
    content = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.plan.name} - {self.content}"

class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    opay_subscription_id = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.end_date and self.plan:
            self.end_date = self.start_date + timezone.timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.end_date < timezone.now() if self.end_date else False

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

class PaymentTransaction(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    )
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_ref = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_ref} - {self.status}"