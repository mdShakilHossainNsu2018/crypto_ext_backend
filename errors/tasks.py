from datetime import datetime, timedelta

from celery import shared_task

from errors.models import ErrorData


@shared_task
def clean_up_error_object():
    ErrorData.objects.filter(created_at__lte=datetime.now() - timedelta(days=3)).delete()
