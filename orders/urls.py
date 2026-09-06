from django.urls import path
from .views import create_order, detail_receipt, all_receipts

urlpatterns = [
    path('create/', create_order, name="create_order"),
    path('receipt/all/', all_receipts, name="all_receipts"),
    path('receipt/<uuid:receipt_number>/', detail_receipt, name='receipt_detail'),
]