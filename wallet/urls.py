from django.urls import path
from .views import wallet_detail, wallet_deposit
urlpatterns = [
    path('balance/', wallet_detail, name="detail_wallet"),
    path('deposit/', wallet_deposit, name="deposit_wallet")
]