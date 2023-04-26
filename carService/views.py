from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


from .models import CustomUser, District, Address, Order, OrderAnalysis
from .serializers import CustomUserSerializer, DistrictSerializer, AddressSerializer, OrderSerializer, OrderAnalysisSerializer

from jose import jwt

import datetime
from dateutil.relativedelta import relativedelta


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderAnalysisViewSet(viewsets.ModelViewSet):
    queryset = OrderAnalysis.objects.all()
    serializer_class = OrderAnalysisSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    try:
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        payload = jwt.decode(token, key=settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
    except jwt.JWTError:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user_data = CustomUser.objects.get(pk=payload['user_id'])
        serializer = CustomUserSerializer(user_data)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def send_notification(request):
    current_time = datetime.datetime.now()

    queue_group_name = "orders"
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(queue_group_name, {"type": "orders_message", 'message': "hey!!!"})
    return Response({"": ""})


@api_view(['GET'])
def test_view(request):
    current_time = datetime.datetime.now()

    print(current_time.time())
    l = OrderAnalysis.objects.filter(time_interval_end__lte=current_time.time())
    print(l)

    # today_date = datetime.datetime.now()
    # date_start = today_date.replace(hour=0, minute=00, second=00)
    # date_end = today_date.replace(hour=23, minute=59, second=00)

    # while date_start < date_end:
    #     OrderAnalysis.objects.create(time_interval_start=date_start.time(), time_interval_end=(date_start + relativedelta(minutes=60)).time(), district=District.objects.get(pk=1))
    #     date_start = date_start + relativedelta(minutes=60)

    return Response({"": ""})
