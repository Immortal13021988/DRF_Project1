from datetime import timedelta

from celery import shared_task
from celery.utils.time import timezone

from users.models import User


@shared_task
def deactivate_users():
    """Блокировка пользователя"""
    users = User.objects.all()
    for user in users:
        if timezone.now() - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
