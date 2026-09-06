from django.db import models
from django.core.validators import RegexValidator

class User(models.Model):
    ROLE_CHOICES = [
        ('customer', 'Покупатель'),
        ('seller', 'Продавец'),
    ]

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате +77777777777 (до 15 цифр)"
    )

    name = models.CharField(max_length=100, verbose_name="Имя") # Исправлено на CharField
    age = models.PositiveIntegerField(verbose_name="Возраст")
    phone = models.CharField(validators=[phone_regex], max_length=30, blank=True, null=True, verbose_name="Номер телефона")
    address = models.CharField(max_length=100, verbose_name="Адрес") # Исправлена опечатка в verbose_name
    email = models.EmailField(unique=True, verbose_name="Почта")
    password = models.CharField(max_length=255, verbose_name="Пароль")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer', verbose_name="Роль пользователя")

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
