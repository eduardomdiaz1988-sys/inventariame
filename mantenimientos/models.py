# mantenimientos/models.py
from django.db import models
from django.contrib.auth.models import User

class Mantenimiento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mantenimientos")
    fecha = models.DateField()
    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"
        ordering = ["-fecha"]
        constraints = [
            models.UniqueConstraint(fields=["usuario", "fecha"], name="unique_mantenimiento_usuario_fecha"),
        ]

    def __str__(self):
        return f"{self.usuario} → {self.fecha} → {self.cantidad}"

class ConfiguracionMantenimientos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    año = models.IntegerField()
    mes = models.IntegerField()
    dias_festivos = models.IntegerField(default=0)

    class Meta:
        unique_together = ("usuario", "año", "mes")

    def __str__(self):
        return f"{self.usuario} {self.mes}/{self.año} → {self.dias_festivos} festivos"
