# Create your tasks here


from celery import shared_task

from crypto_ext_backend.celery import app as celery_app


@celery_app.task
def test_task():
    print("Test print celery")

