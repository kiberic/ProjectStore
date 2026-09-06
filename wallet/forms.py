from django import forms
from .models import Wallet

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Сумма пополнения", min_value=1.00)
    