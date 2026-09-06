from django.db import models
from customers.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Баланс кошелька")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания кошелька")

    def __str__(self):
        return f"Баланс пользователя {self.user.name}: {self.balance} тг."

@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)