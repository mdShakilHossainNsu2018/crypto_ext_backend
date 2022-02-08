

Commands
```shell

docker run -p 6379:6379 -d redis:5

python manage.py migrate django_celery_results

# not recommended for production
celery -A crypto_ext_backend worker -l INFO -B

# recommended for production 
celery -A crypto_ext_backend worker -l INFO 
celery -A crypto_ext_backend beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
