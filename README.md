

Commands
```shell

docker run -p 6379:6379 -d redis:5

python manage.py migrate django_celery_results

# not recommended for production
celery -A crypto_ext_backend worker -l INFO -B

# recommended for production 
celery -A crypto_ext_backend worker -l INFO 
celery -A crypto_ext_backend beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

docker-compose logs -t -f --tail 5

https://stackoverflow.com/questions/19581059/misconf-redis-is-configured-to-save-rdb-snapshots

Using redis-cli, you can stop it trying to save the snapshot:
config set stop-writes-on-bgsave-error no

```
