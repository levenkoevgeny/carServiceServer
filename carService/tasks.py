from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import datetime


@shared_task
def say_hello():
    queue_group_name = "orders"
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(queue_group_name, {"type": "orders_message", 'message': "hey!!!"})


@shared_task
def send_best_district():
    from carService.models import OrderAnalysis
    current_time = datetime.datetime.now().time()
    best_district_for_this_time = OrderAnalysis.objects.filter(time_interval_start__lte=current_time,
                                                               time_interval_end__gte=current_time).first()

    if best_district_for_this_time:
        queue_group_name = "orders"
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(queue_group_name, {"type": "orders_message",
                                                                   'message': best_district_for_this_time.district.district_name})
