from datetime import datetime, timedelta

from celery import shared_task

from core.models import CryptoData


@shared_task
def clean_up_core_object():
    CryptoData.objects.filter(created_at__lte=datetime.now() - timedelta(days=3)).delete()
