from django.db import models
from locations.models import Address

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True, related_name="clientes_principal"
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nombre
