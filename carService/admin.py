from django.contrib import admin
from .models import CustomUser, District, Address, Order, OrderAnalysis
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    pass


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(District)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderAnalysis)