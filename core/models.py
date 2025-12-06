from django.db import models
from django.contrib.auth.models import User
from locations.models import Address
from clientes.models import Cliente


class Cita(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='citas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='citas')
    direccion = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='citas')
    fecha = models.DateTimeField()
    recordatorio = models.BooleanField(default=False)
    venta = models.ForeignKey('sales.Venta', on_delete=models.SET_NULL, null=True, blank=True, related_name='citas')

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"

    def __str__(self):
        return f"Cita con {self.cliente} el {self.fecha:%Y-%m-%d %H:%M}"
