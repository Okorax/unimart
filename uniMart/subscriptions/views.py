from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings
from django.utils import timezone
from .models import SubscriptionPlan, PaymentTransaction

@login_required
def subscribe(request, plan_id):
    try:
        plan = SubscriptionPlan.objects.get(id=plan_id)
    except SubscriptionPlan.DoesNotExist:
        return JsonResponse({"error": "Plan not found"}, status=404)

    if request.method == "POST":
        payloaded = {
            "amount": {
                "currency": "NGN",
                "total":400
            },
            "reference": f"sub_{request.user.id}_{int(timezone.now().timestamp())}",
            "product":{"description":"dd","name":"name"},
            #"customerEmail": request.user.email,
            "payMethod":"BankTransfer",
            "UserPhone": "08169976046",
            #"description": f"Subscription to {plan.name}",
            "callbackUrl": f"{settings.SITE_URL}/plan/callback/",
            #"returnUrl": f"{settings.SITE_URL}/plan/success/",
            #"merchantId": settings.OPAY_MERCHANT_ID,
        }

        payload={
    "amount":{
        "currency":"NGN",
        "total":400
    },
    "callbackUrl":"https://testapi.opaycheckout.com/api/v1/international/print",
    "country":"NG",
    "customerName":"customerName",
    "payMethod":"BankTransfer",
    "product":{
        "description":"dd",
        "name":"name"
    },
    "reference":"12345a",
    "userInfo":{
            "userEmail":"test@email.com",
            "userId":"userid001",
            "userMobile":"+23488889999",
            "userName":"David"
    },
    "userPhone":"+1234567879",
    "merchantId": settings.OPAY_MERCHANT_ID,
}
        headers = {"Authorization": f"Bearer 22763bcdb0260789b61305c183ade61dddb21b74a7b41d76ed487042f7e978f957e544df938a21e89eeb9dc0a4c3cdf561d09eef26c128695c4165fa9f9f9781", "Content-Type": "application/json", "MerchantId": "256612345678901"}

        try:
            response = requests.post(f"{settings.OPAY_API_URL}/international/cashier/create", json=payload, headers=headers)
            data = response.json()
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