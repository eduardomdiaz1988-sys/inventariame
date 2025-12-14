# calendario/admin.py
from django.contrib import admin
from .models import Festivo

@admin.register(Festivo)
class FestivoAdmin(admin.ModelAdmin):
    list_display = ("fecha",)
    search_fields = ("fecha",)
