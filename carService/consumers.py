import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class OrderDataConsumer(WebsocketConsumer):
    group_name = "orders"

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    def receive(self, text_data):
        pass

    def orders_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))