from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
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
