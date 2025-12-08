from django.db import models
from django.contrib.auth.models import User
from locations.models import Address

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True, null=True)  # NUEVO CAMPO
    direccion = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clientes_principal"
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="clientes",
        null=True,  # permite nulos en registros antiguos
        blank=True  # permite dejarlo vacío en formularios
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.nombre} ({self.telefono or 'sin teléfono'})"
