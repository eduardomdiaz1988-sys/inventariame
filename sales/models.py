# sales/models.py
from django.db import models
from django.contrib.auth.models import User
from referencias.models import Referencia
import datetime

class Venta(models.Model):
    referencia = models.ForeignKey(
        Referencia,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ventas"
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ventas")
    fecha = models.DateField(null=True, blank=True, default=datetime.date.today)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def __str__(self):
        return f"{self.referencia} - {self.usuario} ({self.fecha})"
