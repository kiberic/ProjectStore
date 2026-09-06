from django.db import models
from django.core.validators import MaxValueValidator
from django.utils import timezone
import datetime
from dateutil.relativedelta import relativedelta

class CategoryProduct(models.Model):
    CATEGORY_CHOICES=[
        ("vegetables", "Овощи и фрукты"),
        ("meat", "Мясо и птица"),
        ("fish", "Рыба и морепродукты"),
        ("dairy", "Молочные продукты"),
        ("bakery", "Хлеб и выпечка"),
        ("grains", "Крупы, макароны и бобовые"),
        ("oil_sauces", "Масла и соусы"),
        ("canned", "Консервы и заготовки"),
        ("snacks", "Сладости и снеки"),
        ("drinks", "Напитки"),
        ("alcohol", "Алкогольные напитки"),
        ("frozen", "Замороженные продукты"),
        ("spices", "Специи и приправы"),
        ("baby_food", "Детское питание"),
        ("healthy", "Диетические и здоровые продукты"),
        ("household", "Хозяйственные товары"),
    ]
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, verbose_name="Категория продукта")

    def __str__(self):
        return f"Категория: {self.name}"

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование товара")
    body = models.TextField(verbose_name="Описание товара")
    image = models.ImageField(upload_to="products_image/", blank=False, null=False, verbose_name="Примерное фото товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена товара")
    quantity = models.PositiveBigIntegerField(default=0, verbose_name="Количество товара", validators=[MaxValueValidator(30)])
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, verbose_name="Категория продукта")
    date_manufacture = models.DateField(verbose_name="Дата изготовления")
    expiration_date = models.PositiveIntegerField(verbose_name="Срок годности")

    def is_expired(self):
        end_date = self.date_manufacture + relativedelta(months=self.expiration_date)
        return timezone.now().date() > end_date

    def __str__(self):
        return f"{self.name}"