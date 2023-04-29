from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import CustomUser, District, Address, Order, OrderAnalysis
from .serializers import CustomUserSerializer, CustomUserSerializerForSelect2, DistrictSerializer, AddressSerializer, AddressSerializerForSelect2, OrderSerializer, \
    OrderAnalysisSerializer, UserNamesSerializer

from jose import jwt
import json

import datetime
from dateutil.relativedelta import relativedelta
from faker import Faker
import random


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filterset_fields = {'username': ['icontains'],
                        'last_name': ['icontains'],
                        'is_superuser': ['exact'],
                        'is_staff': ['exact'],
                        'is_active': ['exact'],
                        'user_type': ['exact'],
                        }


class UserNamesViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserNamesSerializer
    filterset_fields = {
        'username': ['exact'],
    }


class CustomUserViewSetForSelect2(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializerForSelect2
    filterset_fields = {'user_type': ['exact'], 'last_name': ['icontains']}


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filterset_fields = {'address': ['icontains']}


class AddressViewSetForSelect2(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializerForSelect2
    filterset_fields = {'address': ['icontains']}


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = {'order_status': ['exact'], 'driver': ['exact']}

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
    current_time = datetime.datetime.now().time()

    best_district_for_this_time = OrderAnalysis.objects.filter(time_interval_start__lte=current_time,
                                                               time_interval_end__gte=current_time).first()

    if best_district_for_this_time:
        queue_group_name = "orders"
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(queue_group_name, {"type": "orders_message",
                                                                   'message': best_district_for_this_time.district.district_name})
    return Response({"": ""})


@api_view(['GET'])
def order_analysis(request):
    class Result:
        def __init__(self, district_id, count):
            self.district_id = district_id
            self.count = count

        def __repr__(self):
            return str(self.district_id) + ', ' + str(self.count)

    for analysis in OrderAnalysis.objects.all():

        orders_filtered_by_time = []

        orders = Order.objects.all()
        for order in orders:
            if analysis.time_interval_start <= order.date_time_ordered.time() <= analysis.time_interval_end:
                orders_filtered_by_time.append(order.id)

        orders_qs = Order.objects.filter(pk__in=orders_filtered_by_time)

        result_list = []
        for district in District.objects.all():
            result_list.append(Result(district.id, orders_qs.filter(address_from__district=district).count()))
        result_list.sort(key=lambda x: x.count, reverse=True)

        if len(result_list) > 0:
            best_district = District.objects.get(pk=result_list[0].district_id)
            analysis.district = best_district
            analysis.save()

    return Response({"": ""})


@api_view(['GET'])
def get_chart_data_timing(request):

    result_list_timing = [["Время", "Количество заказов"]]
    result_list_districts = [["Район", "Количество заказов"]]

    for analysis in OrderAnalysis.objects.all():
        orders_filtered_by_time = []
        orders = Order.objects.all()
        for order in orders:
            if analysis.time_interval_start <= order.date_time_ordered.time() <= analysis.time_interval_end:
                orders_filtered_by_time.append(order.id)

        orders_qs = Order.objects.filter(pk__in=orders_filtered_by_time)
        result_list_timing.append([str(analysis.time_interval_start.hour) + ' - ' + str(analysis.time_interval_end.hour) + 'ч.', orders_qs.count()])

    for district in District.objects.all():
        result_list_districts.append([district.district_name, Order.objects.filter(address_from__district=district).count()])

    return Response({"chart_data_timing": result_list_timing, "chart_data_districts": result_list_districts})


@api_view(['GET'])
def init_db(request):
    districts = ["Вокзал", "Серебрянка", "Малиновка",
                 "Уручье", "Тракторный завод",
                 "Новая Боровая", "Автозавод", "Шабаны", "Каменная горка", "Центр", "Асмоловка"]
    try:
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=10)
        District.objects.all().delete()

        for district in districts:
            District.objects.create(district_name=district)
        Address.objects.all().delete()
        Order.objects.all().delete()

        Faker.seed(random.randint(1, 99999))
        fake = Faker(['ru-RU'])

        districts = District.objects.all()
        districts_ids = list(District.objects.all().values_list('id', flat=True))
        for i in range(1000):
            random_id = random.randint(0, len(districts_ids))
            random_district = districts.get(pk=districts_ids[random_id - 1])
            Address.objects.create(address=fake.street_address(), district=random_district)

        addresses = Address.objects.all()
        addresses_ids = list(Address.objects.all().values_list('id', flat=True))
        for i in range(1000):
            random_id_address = random.randint(0, len(addresses_ids))
            random_address_from = addresses.get(pk=addresses_ids[random_id_address - 1])
            random_id_address = random.randint(0, len(addresses_ids))
            random_address_to = addresses.get(pk=addresses_ids[random_id_address - 1])
            random_date = start_date + (end_date - start_date) * random.random()
            Order.objects.create(date_time_ordered=random_date, address_from=random_address_from,
                                 address_to=random_address_to)

        OrderAnalysis.objects.all().delete()
        today_date = datetime.datetime.now()
        date_start = today_date.replace(hour=0, minute=00, second=00, microsecond=0)
        date_end = today_date.replace(hour=23, minute=59, second=00, microsecond=0)
        # random_id = random.randint(0, len(districts_ids))
        # random_district = districts.get(pk=districts_ids[random_id - 1])

        while date_start < date_end:
            OrderAnalysis.objects.create(time_interval_start=date_start.time(),
                                         time_interval_end=(date_start + relativedelta(minutes=60)).time())
            date_start = date_start + relativedelta(minutes=60)

    except Exception as err:
        return Response({"message": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"message": "DB init Ok"}, status=status.HTTP_200_OK)
