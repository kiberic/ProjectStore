from django.shortcuts import render, redirect
from .models import Order, OrderItem, Receipt
from customers.models import User
from products.models import Product
from django.contrib import messages
from django.db import transaction

def create_order(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        request.session.flush()
        return redirect("login")

    # --- СЦЕНАРИЙ 1: Нажата кнопка «Оформить» из каталога ---
    if request.method == "POST" and "confirm_payment" not in request.POST:
        product_ids = request.POST.getlist("product_ids")
        if not product_ids:
            messages.error(request, "Вы не выбрали ни одного товара.")
            return redirect("all_products")

        checkout_product = {}
        for prod_id in product_ids:
            quant = int(request.POST.get(f"quantity_{prod_id}", 1))
            if quant > 0:
                checkout_product[str(prod_id)] = quant

        if not checkout_product:
            messages.error(request, "Вы не выбрали ни одного товара.")
            return redirect("all_products")

        request.session["temporary_cart"] = checkout_product
        return redirect("create_order")

    # --- СЦЕНАРИЙ 2: Нажата кнопка «Подтвердить и оплатить» на странице чека ---
    if request.method == "POST" and "confirm_payment" in request.POST:
        checkout_product = request.session.get("temporary_cart")
        if not checkout_product:
            messages.error(request, "Ваша корзина пуста или истекла сессия.")
            return redirect("all_products")
        
        total_cost = 0
        items_to_buy = []

        for product_id, quantity in checkout_product.items():
            quantity = int(quantity)
            if quantity <= 0: 
                continue

            try:
                product = Product.objects.get(id=int(product_id))
            except Product.DoesNotExist:
                messages.error(request, "Один из товаров не найден.")
                return redirect("all_products")

            if product.quantity < quantity:
                messages.error(request, f"Недостаточно товара {product.name} на складе. Доступно: {product.quantity} шт.")
                return redirect("all_products")

            total_cost += product.price * quantity
            items_to_buy.append((product, quantity))

        if not items_to_buy:
            messages.error(request, "Ошибка формирования заказа.")
            return redirect("all_products")

        wallet = user.wallet
        if wallet.balance < total_cost:
            messages.error(request, "Недостаточно баланса на кошельке для оплаты.")
            return redirect("create_order")

        with transaction.atomic():
            wallet.balance -= total_cost
            wallet.save()

            order = Order.objects.create(user=user, status="new")

            for product, quantity in items_to_buy:
                product.quantity -= quantity
                product.save()

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=quantity
                )

            Receipt.objects.create(
                order=order,
                amount_paid=total_cost
            )
        
        del request.session["temporary_cart"]
        messages.success(request, f"Заказ №{order.id} на сумму {total_cost} тг. успешно оформлен.")
        return redirect("all_products")

    # --- СЦЕНАРИЙ 3: Отрисовка страницы (GET-запрос) ---
    checkout_product = request.session.get("temporary_cart", {})
    if not checkout_product:
        messages.error(request, "Нет активных сессий оформления заказа.")
        return redirect("all_products")

    order_items = []
    total_cost = 0

    for product_id, quantity in checkout_product.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = product.price * quantity
            total_cost += item_total
            order_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })
        except Product.DoesNotExist:
            continue

    context = {
        'order_items': order_items,
        'total_cost': total_cost,
        'user': user
    }
    return render(request, "create_order.html", context)


def detail_receipt(request, receipt_number):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    current_user = User.objects.get(id=user_id)

    try:
        receipt = Receipt.objects.select_related('order__user').get(receipt_number=receipt_number)
    except Receipt.DoesNotExist:
        messages.error(request, "Чек не найден")
        return redirect("all_receipts")
    if current_user.role != 'seller' and receipt.order.user != current_user:
        messages.error(request, "У вас нет прав на просмотра этого чека")
        return redirect("all_products")

    return render(request, "detail_receipts.html", {"receipt" : receipt})

def all_receipts(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)

    if user.role == 'seller':
        receipts = Receipt.objects.select_related('order__user').all().order_by('-created_at')
    else:
        receipts = Receipt.objects.filter(order__user=user).order_by('-created_at')

    return render(request, "all_receipts.html", {"receipts" : receipts})