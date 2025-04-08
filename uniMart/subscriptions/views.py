import hmac
import hashlib
import json
import requests
import time
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings
from django.utils import timezone
from .models import SubscriptionPlan, PaymentTransaction

OPAY_SANDBOX_URL = "https://test-api.opayweb.com/api/v3/"  # Try this instead

@login_required
def subscribe(request, plan_id):
    try:
        plan = SubscriptionPlan.objects.get(id=plan_id)
    except SubscriptionPlan.DoesNotExist:
        return JsonResponse({"error": "Plan not found"}, status=404)

    if request.method == "POST":
        ref = f"dep_{request.user.id}_{int(time.time())}"
        payload = {
            "amount": str(int(1000 * 100)),  # Convert to kobo
            "callbackUrl": "https://yourapp.com/deposit/callback/",
            "country": "NG",
            "currency": "NGN",
            "customerEmail": request.user.email or "test@example.com",
            "customerPhone": "08012345678",  
            "description": f"Deposit of ₦1000 to wallet via bank transfer",
            "paymentMethod": "BANK",           # Set to bank transfer
            "reference": ref,
            "returnUrl": "https://yourapp.com/deposit/success/"
        }

        payload_string = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        signature = hmac.new(
            settings.OPAY_SECRET_KEY.encode(), 
            payload_string.encode(), 
            hashlib.sha512
        ).hexdigest()

        headers = {
            "Authorization": f"Bearer {settings.OPAY_PUBLIC_KEY}",  # Use public key or token, not signature
            "MerchantId": settings.OPAY_MERCHANT_ID,
            "Content-Type": "application/json",
            #"Signature": signature  # Uncomment if OPay docs specify a Signature header
        }

        try:
            #response = requests.post(f"{settings.OPAY_API_URL}/international/cashier/create", json=payload, headers=headers)
            #data = response.json()
            response = requests.post(f"{settings.OPAY_API_URL}/international/cashier/create", headers=headers, json=payload)
            data = response.json()
            for _ in range(3000):
                print(data)
            if data.get("code") == "00000":
                transaction = PaymentTransaction.objects.create(
                    user_subscription=None,
                    amount=plan.price,
                    transaction_ref=payload["reference"],
                )
                return redirect(data["data"]["cashierUrl"])
            else:
                return JsonResponse({"error": "Payment initiation failed"}, status=400)
        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "subscriptions/subscribe.html", {"plan": plan, "items": plan.items.all()})