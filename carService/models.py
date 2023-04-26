from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # subdivision = models.ForeignKey(Subdivision, on_delete=models.CASCADE)

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

    class Meta:
        ordering = ('address',)
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адресы'


class Order(models.Model):
    date_time_ordered = models.DateTimeField(verbose_name="Дата и время заказа")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="Адрес")

    def __str__(self):
        return str(self.date_time_ordered) + ' ' + self.address.address

    class Meta:
        ordering = ('address',)
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
