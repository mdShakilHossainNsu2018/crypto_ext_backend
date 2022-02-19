# chat/routing.py

from . import consumers
from django.urls import path

# ws://127.0.0.1:8000/ws/binance/btc/
websocket_urlpatterns = [
    path('ws/eth_gas/all/', consumers.EthGASConsumer.as_asgi()),
]

