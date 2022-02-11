import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from crypto_ext_backend.celery import app
import requests
from crypto_ext_backend.settings import BTC_GROUP, CRYPTO_GROUP, CRYPTO_ROOM


@app.task
def send_crypto_message():
    # Send message to room group
    # {"symbol": "BTCUSDT", "price": "43592.48000000"},
    channel_layer = get_channel_layer()
    r = requests.get("https://api.binance.com/api/v3/ticker/price")
    print(r.text)
    json_res = r.json()

    async_to_sync(channel_layer.group_send)(
        # Broadcast to crypto group
        CRYPTO_GROUP,
        {
            'type': 'chat_message',
            'message': json_res
        }
    )

    for obj in json_res:
        if obj["symbol"] == "BTCUSDT":
            print(obj["price"])
            async_to_sync(channel_layer.group_send)(
                # It is the btc group name
                "group_" + BTC_GROUP,
                {
                    'type': 'chat_message',
                    'message': obj["price"]
                }
            )


class BTCConsumer(WebsocketConsumer):
    def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_name = BTC_GROUP
        self.room_group_name = 'group_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


class AllCryptoConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = CRYPTO_GROUP
        self.room_name = CRYPTO_ROOM

    def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_name = CRYPTO_ROOM
        self.room_group_name = CRYPTO_GROUP

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
