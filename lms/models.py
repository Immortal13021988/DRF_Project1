from django.db import models

from config import settings


class Course(models.Model):
    title = models.CharField(
        max_length=100, verbose_name="Курс", help_text="Введите название курса"
    )
    preview = models.ImageField(
        upload_to="lms/course/photo",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Заполните описание",
        blank=True,
        null=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Владелец",
        help_text="Укажите владельца",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(
        max_length=100, verbose_name="Урок", help_text="Введите название урока"
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Заполните описание",
        blank=True,
        null=True,
    )
    preview = models.ImageField(
        upload_to="lms/lesson/photo",
        blank=True,
        null=True,
    )
    video_url = models.URLField(
        max_length=200,
        verbose_name="Ссылка на видео",
        help_text="Скопируйте ссылку на видео",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        "Course",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Курс",
        help_text="Выберите курс",
        related_name="lessons",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Владелец",
        help_text="Укажите владельца",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
