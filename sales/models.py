# sales/models.py
from django.db import models
from django.conf import settings
from oferta.models import Oferta

class Venta(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name="ventas")
    cantidad = models.PositiveIntegerField(default=1)
    mantenimiento_numero = models.IntegerField(null=True, blank=True, help_text="Número de mantenimiento asociado (opcional)")
    ppa = models.BooleanField(default=False, help_text="Marcar si la venta ha convertido PPA")
    
    def __str__(self):
        return f"Venta {self.id} - {self.oferta.nombre}"
