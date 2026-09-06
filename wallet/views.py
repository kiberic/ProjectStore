from django.shortcuts import render, redirect
from django.contrib import messages
from customers.models import User
from .forms import DepositForm
from django.db import transaction

def wallet_detail(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)
    wallet = user.wallet
    
    return render(request, "detail_wallet.html", {"wallet": wallet})


def wallet_deposit(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get("amount")

            with transaction.atomic():
                wallet = user.wallet
                wallet.balance += amount
                wallet.save()

            messages.success(request, f"Баланс кошелька успешно пополнен на сумму {amount}. Текущий баланс: {wallet.balance}")
            return redirect("all_products")
    else:
        form = DepositForm()
    return render(request, "wallet_deposit.html", {"form": form})