from django.db import models
from referencias.models import Referencia, Tipo

class Oferta(models.Model):
    nombre = models.CharField(max_length=150)
    referencia = models.ForeignKey(
        Referencia,
        on_delete=models.CASCADE,
        related_name="ofertas",
        default=1
    )
    tipo = models.ForeignKey(
        Tipo,
        on_delete=models.CASCADE,
        related_name="ofertas",
        default=1
    )
    valor = models.CharField(
        max_length=50,
        help_text="Expresión como '0 + 7', '0 + 3', etc."
    )

    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.tipo}) - {self.valor}"
