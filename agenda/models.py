# agenda/models.py
from django.db import models
from django.conf import settings

class EventoAgenda(models.Model):
    TIPO_CHOICES = [
        ("cita", "Cita"),
        ("venta", "Venta"),
        ("otro", "Otro"),
    ]
    titulo = models.CharField(max_length=200)
    inicio = models.DateTimeField()
    fin = models.DateTimeField(null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="otro")
    referencia_id = models.PositiveIntegerField(null=True, blank=True)  # id de cita/venta
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["inicio"]

    def __str__(self):
        return f"{self.titulo} ({self.tipo})"
