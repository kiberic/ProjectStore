from django.db import models
from products.models import Product

class Inventory(models.Model):
    TRANZACTION_TYPES = [
        ('receipt', 'Поставка'),
        ('write_off', 'Списание'),
        ('correction', 'Корректировка')
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    tranzaction_type = models.CharField(max_length=20, choices=TRANZACTION_TYPES, verbose_name="Тип операции")
    quantity_changed = models.PositiveBigIntegerField(verbose_name="Количество")
    document_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Номер накладной / Документа")
    reason = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время операции")

    def __str__(self):
        return f"{self.get_tranzaction_type_display()} - {self.product.name} ({self.quantity_changed} шт.)"