import json
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import requests
from crypto_ext_backend.settings import BTC_GROUP, CRYPTO_GROUP, CRYPTO_ROOM, CRYPTO_ALARM_ROOM, CRYPTO_ALARM_GROUP
from errors.models import ErrorData, Errors
from channels.db import database_sync_to_async


async def async_task():
    # Send message to room group
    # {"symbol": "BTCUSDT", "price": "43592.48000000"},
    channel_layer = await get_channel_layer()
    r = requests.get("https://api.binance.com/api/v3/ticker/price")
    # print(r.text)
    json_res = await r.json()

    await channel_layer.group_send(
        # Broadcast to crypto group
        CRYPTO_GROUP,
        {
            'type': 'chat_message',
            'message': json_res
        }
    )
    BTCUSDT = 0
    # ETHBTC = 0
    # ETHUSDT = 0
    # BNBETH = 0
    # ETHTUSD = 0
    # TUSDBNB = 0

    all_pair_dict = {}

    for obj in json_res:
        all_pair_dict[obj["symbol"]] = obj["price"]

        if obj["symbol"] == "BTCUSDT":
            BTCUSDT = obj["price"]
        # if obj["symbol"] == "ETHBTC":
        #     ETHBTC = obj["price"]
        # if obj["symbol"] == "ETHUSDT":
        #     ETHUSDT = obj["price"]
        # if obj["symbol"] == "BNBETH":
        #     BNBETH = obj["price"]
        # if obj["symbol"] == "ETHTUSD":
        #     ETHTUSD = obj["price"]
        # if obj["symbol"] == "TUSDBNB":
        #     TUSDBNB = obj["price"]

    # alarm_obj = {
    #     "BTCUSDT": BTCUSDT,
    #     "ETHBTC": ETHBTC,
    #     "ETHUSDT": ETHUSDT,
    #     "BNBETH": BNBETH,
    #     "ETHTUSD": ETHTUSD,
    #     "TUSDBNB": TUSDBNB
    # }

    await channel_layer.group_send(
        # It is the btc group name
        CRYPTO_ALARM_GROUP,
        {
            'type': 'chat_message',
            'message': all_pair_dict
        }
    )

    await channel_layer.group_send(
        # It is the btc group name
        "group_" + BTC_GROUP,
        {
            'type': 'chat_message',
            'message': BTCUSDT
        }
    )


@shared_task
def send_crypto_message():
    async_to_sync(async_task())()


class BTCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_name = BTC_GROUP
        self.room_group_name = 'group_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


class AllCryptoConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = CRYPTO_GROUP
        self.room_name = CRYPTO_ROOM

    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_name = CRYPTO_ROOM
        self.room_group_name = CRYPTO_GROUP

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


class CryptoAlarmConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = CRYPTO_ALARM_GROUP
        self.room_name = CRYPTO_ALARM_ROOM

    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_name = CRYPTO_ALARM_ROOM
        self.room_group_name = CRYPTO_ALARM_GROUP

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
