# referencias/models.py
from django.db import models

class Tipo(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Tipo"
        verbose_name_plural = "Tipos"

    def __str__(self):
        return self.nombre


class Referencia(models.Model):
    nombre = models.CharField(max_length=150)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, related_name="referencias")
 
    class Meta:
        verbose_name = "Referencia"
        verbose_name_plural = "Referencias"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"
