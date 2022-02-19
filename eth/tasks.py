from datetime import datetime, timedelta

from celery import shared_task

from eth.models import EthGASData, BaseAndPriorityFee


@shared_task
def clean_up_eth_object():
    EthGASData.objects.filter(created_at__lte=datetime.now() - timedelta(days=3)).delete()
    BaseAndPriorityFee.objects.filter(created_at__lte=datetime.now() - timedelta(days=3)).delete()
