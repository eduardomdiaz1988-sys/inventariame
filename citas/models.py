from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente
from oferta.models import Oferta   # Importamos Oferta

class Cita(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("completada", "Completada"),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='citas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='citas')
    fecha = models.DateTimeField()
    recordatorio = models.BooleanField(default=False, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente", blank=True)
    numero_instalacion = models.IntegerField(default=0)
    observaciones = models.TextField(blank=True, null=True)

    ofertas = models.ManyToManyField(Oferta, through="CitaOferta", related_name="citas")

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"

    def __str__(self):
        return f"Cita con {self.cliente} el {self.fecha:%Y-%m-%d %H:%M} ({self.estado})"

class CitaOferta(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name="cita_ofertas")
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.oferta.nombre} x{self.cantidad}"
