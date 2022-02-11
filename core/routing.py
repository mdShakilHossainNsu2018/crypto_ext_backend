# chat/routing.py

from . import consumers
from django.urls import path

# ws://127.0.0.1:8000/ws/binance/btc/
websocket_urlpatterns = [
    path('ws/binance/btc/', consumers.BTCConsumer.as_asgi()),
    path('ws/binance/all/price/', consumers.AllCryptoConsumer.as_asgi()),
]

