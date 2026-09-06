from django.db import models
from customers.models import User
from products.models import Product
import uuid

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Заказчик")
    STATUS_CHOICES = [
        ("new", "Новый"),
        ('payment_pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('in_progress', 'В обработке / Сборка'),
        ('shipped', 'Отправлен / В пути'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменен'),
        ('returned', 'Возврат'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="new", verbose_name="Статус заказа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveBigIntegerField()

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name}x{self.quantity} - {self.get_cost()} тг."

class Receipt(models.Model): # чек о оформлении заказа
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    receipt_number = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name="Номер чека")
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма к оплате")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания чека")

    def __str__(self):
        return f"Чек {self.receipt_number}: Заказ оплочен на сумму {self.amount_paid} тг."