# sales/models.py
from django.db import models
from django.conf import settings
from oferta.models import Oferta

class Venta(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    # ✅ ahora una venta puede tener varias ofertas con cantidades
    ofertas = models.ManyToManyField(Oferta, through="VentaOferta", related_name="ventas")
    mantenimiento_numero = models.IntegerField(null=True, blank=True, help_text="Número de mantenimiento asociado (opcional)")
    ppa = models.BooleanField(default=False, help_text="Marcar si la venta ha convertido PPA")

    def __str__(self):
        # mostramos las ofertas asociadas con sus cantidades
        ofertas_str = ", ".join(
            f"{vo.oferta.nombre} x{vo.cantidad}" for vo in self.venta_ofertas.all()
        )
        return f"Venta {self.id} - {ofertas_str if ofertas_str else 'Sin ofertas'}"


class VentaOferta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="venta_ofertas")
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("venta", "oferta")  # ✅ evita duplicados de la misma oferta en una venta

    def __str__(self):
        return f"{self.oferta.nombre} x{self.cantidad} (Venta {self.venta.id})"
