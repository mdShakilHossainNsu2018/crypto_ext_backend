import json
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
import requests
from crypto_ext_backend.settings import ETH_GAS_GROUP, ETH_GAS_ROOM
from errors.models import Errors, ErrorData
from eth.models import EthGASData, BaseAndPriorityFee


@shared_task
def send_gas_message():
    channel_layer = get_channel_layer()
    # todo: key must store in env
    api_key = "59ee27c6-decc-43d6-9927-cde5d99a58b7"
    api_endpoint = "https://api.blocknative.com/gasprices/blockprices?confidenceLevels=99&confidenceLevels=95" \
                   "&confidenceLevels=80&confidenceLevels=70"
    r = requests.get(api_endpoint, headers={'Authorization': api_key})
    # print(r.text)
    json_res = r.json()

    if r.status_code != 200:
        ErrorData.objects.create(error_from=f"send_gas_message state code {r.status_code}",
                                 message=r.text,
                                 error_type=Errors.TOO_MANY_REQ
                                 )
        print("some thing wrong")
    if r.status_code == 200:
        try:
            block_price_obj = json_res["blockPrices"][0]
            obj_on_80 = block_price_obj["estimatedPrices"][2]
            block_number = block_price_obj["blockNumber"]
            base_fee_per_gas = block_price_obj["baseFeePerGas"]
            max_priority_fee_per_gas = obj_on_80["maxPriorityFeePerGas"]
            BaseAndPriorityFee.objects.create(base_fee=base_fee_per_gas,
                                              max_priority_fee=max_priority_fee_per_gas,
                                              block_number=block_number
                                              )
            # EthGASData.objects.create(data=json_res)
        except Exception as e:
            ErrorData.objects.create(error_from=f"send_gas_message unable to create data",
                                     message=str(e),
                                     error_type=Errors.DB_ERROR
                                     )
            print(e)

        async_to_sync(channel_layer.group_send)(
            # Broadcast to crypto group
            ETH_GAS_GROUP,
            {
                'type': 'chat_message',
                'message': json_res
            }
        )

    # for obj in json_res:
    #     if obj["symbol"] == "BTCUSDT":
    #         print(obj["price"])
    #         async_to_sync(channel_layer.group_send)(
    #             # It is the btc group name
    #             "group_" + BTC_GROUP,
    #             {
    #                 'type': 'chat_message',
    #                 'message': obj["price"]
    #             }
    #         )


class EthGASConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = ETH_GAS_GROUP
        self.room_name = ETH_GAS_ROOM

    def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_name = ETH_GAS_ROOM
        self.room_group_name = ETH_GAS_GROUP

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        eth_gas_data = BaseAndPriorityFee.objects.all()[:100]
        for obj in eth_gas_data:
            async_to_sync(self.channel_layer.group_send)(
                # Broadcast to crypto group
                ETH_GAS_GROUP,
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

    # Receive message from WebSocket
    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #
    #     # Send message to room group
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )

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
