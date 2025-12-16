import random
from datetime import timedelta

from celery import shared_task
from celery.schedules import crontab
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from product.models import Review


@shared_task
def generate_confirmation_code(user_id):
    code = random.randint(100000, 999999)
    key = f"confirm:{user_id}"

    settings.REDIS.set(key, code, ex=300)

    return code


@shared_task
def delete_old_reviews():
    limit_date = timezone.now() - timedelta(days=180)
    Review.objects.filter(created_at__lt=limit_date).delete()


def send_confirmation_email(email, code):
    send_mail(
        subject="Код подтверждения",
        message=f"Ваш код подтверждения: {code}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

