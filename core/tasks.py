from crypto_ext_backend.celery import app


@app.task
def test_task():
    print("Test print celery")

