from django.db import models
from django.contrib.auth.models import User
from core.models import Cliente

class Venta(models.Model):
    referencia = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    instalacion = models.IntegerField(default=0)     # horas o unidades
    mantenimiento = models.IntegerField(default=0)   # horas o unidades
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ventas')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ventas')

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def __str__(self):
        return f"{self.referencia} - {self.cliente}"
