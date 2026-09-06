from django.urls import path
from .views import all_products, detail_product, add_new_product

urlpatterns = [
    path('all/', all_products, name="all_products"),
    path('detail/<int:pk>/', detail_product, name="detail_product"),
    path('add/', add_new_product, name="add_new_product"),
]