# models.py
from django.db import models
from referencias.models import Referencia

class Oferta(models.Model):
    nombre = models.CharField(max_length=150)
    referencia = models.ForeignKey(
        Referencia,
        on_delete=models.CASCADE,
        related_name="ofertas",
        default=1
    )
    valor = models.IntegerField(
        choices=[(3, "0 + 3"), (4, "0 + 4"), (5, "0 + 5"), (7, "0 + 7"), (10, "0 + 10")],
        help_text="Selecciona uno de los valores permitidos"
    )

    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.referencia.tipo.nombre}) - 0 + {self.valor}"
