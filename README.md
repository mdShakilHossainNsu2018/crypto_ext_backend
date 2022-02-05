
```shell

docker run -p 6379:6379 -d redis:5

python manage.py migrate django_celery_results

celery -A crypto_ext_backend worker -l INFO -B

```
