from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    """Модель пользователя"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона",
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatar/",
        verbose_name="Аватар",
        help_text="Выберите файл с фото",
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=30,
        verbose_name="Город",
        help_text="Введите город",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    """Модель платежи"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Выберете пользователя",
        null=True,
        blank=True,
    )
    date_payment = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата платежа",
    )
    course_paid = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        null=True,
        blank=True,
    )
    lesson_paid = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        null=True,
        blank=True,
    )
    amount = models.PositiveIntegerField(
        verbose_name="Сумма оплаты",
        help_text="Укажите сумму оплаты",
    )
    method_payment = models.CharField(
        max_length=20,
        choices=[("cash", "Наличные"), ("transfer", "Перевод на счет")],
        null=True,
        blank=True,
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
    )
    session_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Id сесии",
        help_text="Укажите Id сесии",
    )
    link = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-date_payment"]  # новые платежи первыми

    def __str__(self):
        return f"Платеж {self.user} - {self.amount} руб."
