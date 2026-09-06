from django.shortcuts import render, redirect
from customers.models import User
from django.contrib import messages
from django.db import transaction
from products.models import Product
from .models import Inventory

def manage_invertory(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)

    if user.role != 'seller':
        messages.error(request, "Доступ в раздел склада разрешён только продавцу.")
        return redirect("all_products")

    products = Product.objects.all().order_by('id')

    context = {
        "products": products,
        "tranzaction_types": Inventory.TRANZACTION_TYPES
    }

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        tranzaction_type = request.POST.get("tranzaction_type")
        document_number = (request.POST.get("document_number") or "").strip()
        reason = (request.POST.get("reason") or "").strip()

        try:
            quantity_changed = int(request.POST.get("quantity_changed", 0))
        except (ValueError, TypeError):
            messages.error(request, "Ошибка: введено некорректное число.")
            return render(request, "manage_inventory.html", context)

        if quantity_changed <= 0:
            messages.error(request, "Количество должно быть больше нуля!")
            return render(request, "manage_inventory.html", context)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.error(request, "Выбранный товар не найден.")
            return render(request, "manage_inventory.html", context)

        with transaction.atomic():
            if tranzaction_type == "receipt":
                if product.quantity + quantity_changed > 30:
                    messages.error(request, "Лимит превышен (максимум 30 шт. на складе).")
                    return render(request, "manage_inventory.html", context)
                product.quantity += quantity_changed

            elif tranzaction_type == "write_off":
                if product.quantity < quantity_changed:
                    messages.error(request, "Нельзя списать больше, чем есть на складе.")
                    return render(request, "manage_inventory.html", context)
                product.quantity -= quantity_changed

            elif tranzaction_type == "correction":
                if quantity_changed > 30:
                    messages.error(request, "Нельзя установить больше лимита (30 шт.).")
                    return render(request, "manage_inventory.html", context)
                product.quantity = quantity_changed

            product.save()

            Inventory.objects.create(
                product=product,
                tranzaction_type=tranzaction_type,
                quantity_changed=quantity_changed,
                document_number=document_number,
                reason=reason
            )

        messages.success(request, f"Складская операция для товара «{product.name}» успешно проведена.")
        return redirect("manage_inventory")

    return render(request, "manage_inventory.html", context)