from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        (0, "Обычный пользователь"),
        (1, "Водитель"),
    ]
    avatar = models.ImageField(verbose_name="Аватар", blank=True, null=True, upload_to="avatars")
    user_type = models.IntegerField(verbose_name="Тип пользователя", choices=USER_TYPE_CHOICES, default=0)

    @property
    def text(self):
        return self.last_name if self.last_name else self.username

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class District(models.Model):
    district_name = models.TextField(verbose_name="Название района")

    def __str__(self):
        return self.district_name

    class Meta:
        ordering = ('district_name',)
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'


class Address(models.Model):
    address = models.TextField(verbose_name="Адрес")
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="Район")

    def __str__(self):
        return self.address

    # for select2 options
    @property
    def text(self):
        return self.address

    class Meta:
        ordering = ('address',)
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адресы'


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        (0, "Создан"),
        (1, "Принят к исполнению"),
        (2, "Выполнен"),
    ]
    date_time_ordered = models.DateTimeField(verbose_name="Дата и время заказа")
    address_from = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="address_from", verbose_name="Адрес")
    address_to = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="address_to", verbose_name="Адрес")
    order_status = models.IntegerField(verbose_name="Статус заказа", default=0, choices=ORDER_STATUS_CHOICES)
    driver = models.ForeignKey(CustomUser, verbose_name="Водитель", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date_time_ordered) + ' ' + self.address_from.address + ' ' + self.address_to.address

    @property
    def get_address_from(self):
        return self.address_from.address

    @property
    def get_address_to(self):
        return self.address_to.address

    @property
    def get_driver_info(self):
        return self.driver.last_name if self.driver else 'Нет данных'

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderAnalysis(models.Model):
    time_interval_start = models.TimeField(verbose_name="Начало интервала")
    time_interval_end = models.TimeField(verbose_name="Окончание интервала")
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="Район", blank=True, null=True)

    def __str__(self):
        return str(self.time_interval_start) + ' ' + str(self.time_interval_end) + ' ' + str(self.district)

    class Meta:
        ordering = ('time_interval_start',)
        verbose_name = 'Анализ заказов'
        verbose_name_plural = 'Анализы заказов'
