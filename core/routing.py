# chat/routing.py

from . import consumers
from django.urls import path

websocket_urlpatterns = [
    path('ws/btc/', consumers.BTCConsumer.as_asgi()),
]

