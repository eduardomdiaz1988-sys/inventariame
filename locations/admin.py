from django.contrib import admin
from .models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("address", "label", "latitude", "longitude", "principal", "cliente", "user")
    list_filter = ("principal", "cliente")
