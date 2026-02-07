from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


@shared_task
def send_email_about_update_course(email, course):
    send_mail(
        "Обновление курса",
        f"Материалы курса: '{course}' обновлены! Проверьте свои подписки!",
        EMAIL_HOST_USER,
        [email,],
    )
