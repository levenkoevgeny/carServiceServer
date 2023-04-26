from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task
def say_hello():
    queue_group_name = "orders"
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(queue_group_name, {"type": "orders_message", 'message': "hey!!!"})