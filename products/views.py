from django.shortcuts import render, redirect 
from .models import Product
from customers.models import User
from .forms import ProductForm
from django.contrib import messages

def all_products(request):
    products = Product.objects.all()
    user = None

    user_id = request.session.get("user_id")
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            if "user_id" in request.session:
                del request.session["user_id"]

    context = {
        "products" : products,
        "user" : user
    }
    return render(request, "all_products.html", context)

def detail_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        messages.warning(request, "Товар не найден")
        return redirect("all_products")

    user = None
    user_id = request.session.get("user_id")
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass

    context = {
        "product": product,
        "user": user
    }
    return render(request, "detail_product.html", context)

def add_new_product(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    
    user = User.objects.get(id=user_id)
    
    if user.role == 'customer':
        messages.error(request, "У вас недостаточно прав для добавления новых продуктов")
        return redirect("all_products")
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("all_products")
    else:
        form = ProductForm()
    return render(request, "add_new_product.html", {"form" : form})

