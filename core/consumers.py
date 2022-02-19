import json
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from core.models import CryptoData
import requests
from crypto_ext_backend.settings import BTC_GROUP, CRYPTO_GROUP, CRYPTO_ROOM
from errors.models import ErrorData, Errors
from channels.db import database_sync_to_async


@shared_task
def send_crypto_message():
    # Send message to room group
    # {"symbol": "BTCUSDT", "price": "43592.48000000"},
    channel_layer = get_channel_layer()
    r = requests.get("https://api.binance.com/api/v3/ticker/price")
    # print(r.text)
    json_res = r.json()

    # if r.status_code != 200:
    #     ErrorData.objects.create(error_from=f"send_crypto_message state code {r.status_code}",
    #                              message=r.text,
    #                              error_type=Errors.TOO_MANY_REQ
    #                              )

    # if r.status_code == 200:
    #     # print(r.json())
    #     try:
    #         CryptoData.objects.create(data=json_res)
    #     except Exception as e:
    #         ErrorData.objects.create(error_from=f"send_crypto_message unable to create data",
    #                                  message=str(e),
    #                                  error_type=Errors.DB_ERROR
    #                                  )
    #         print(e)

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

        # Sending initial message

        crypto_data = CryptoData.objects.all()

        for obj in crypto_data:
            async_to_sync(self.channel_layer.group_send)(
                # Broadcast to crypto group
                CRYPTO_GROUP,
                {
                    'type': 'initial_message',
                    'message': obj.as_dict()
                }
            )

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

    def initial_message(self, event):
            message = event['message']

            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'initial_message': message
            }))
