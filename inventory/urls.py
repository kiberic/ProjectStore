from django.urls import path
from .views import manage_invertory

urlpatterns = [
    path('manage/', manage_invertory, name="manage_inventory"),
]