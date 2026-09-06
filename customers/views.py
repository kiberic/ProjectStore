from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import User
from .forms import RegisterForm, LoginForm

def register_view(request):
    if "user_id" in request.session:
        return redirect('all_products')

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            request.session["user_id"] = user.id
            if user.role == "seller":
                messages.success(request, f"Успешная регистрация. Добро пожаловать, продавец {user.name}!")
                return redirect("manage_inventory")
            else:
                messages.success(request, f"Успешная регитрация. Добро пожаловать, клиент {user.name}!")
                return redirect("all_products")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if "user_id" in request.session:
        return redirect("all_products")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    request.session["user_id"] = user.id
                    
                    next_url = request.GET.get("next")
                    if next_url:
                        return redirect(next_url)
                    elif user.role == 'seller':
                        return redirect("manage_inventory")
                    else:
                        return redirect("all_products")                    
                else:
                    messages.error(request, "Неверный пароль.")
            except User.DoesNotExist:
                messages.error(request, "Пользователь с таким email не найден.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

def logout_view(request):
    if request.method == "POST":
        if "user_id" in request.session:
            del request.session["user_id"]
        return redirect("all_products")
    return render(request, "logout_confirm.html")