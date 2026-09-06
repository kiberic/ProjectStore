from django.shortcuts import render


def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def not_found_or_error(request, exception=None):
    return render(request, "error.html", status=404)