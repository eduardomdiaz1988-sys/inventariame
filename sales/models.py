from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente
from referencias.models import Referencia   # Importamos el modelo Referencia

class Venta(models.Model):
    referencia = models.ForeignKey(
        Referencia,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ventas"
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    instalacion = models.IntegerField(default=0)     # horas o unidades
    mantenimiento = models.IntegerField(default=0)   # horas o unidades
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ventas")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="ventas")

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def __str__(self):
        return f"{self.referencia} - {self.cliente}"
