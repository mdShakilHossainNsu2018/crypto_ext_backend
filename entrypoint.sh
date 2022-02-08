#!/bin/sh

python manage.py makemigrations
python manage.py migrate


daphne -p 8001 crypto_ext_backend.asgi:application