from django.db import models
from django.contrib.auth.models import User

class Elemento(models.Model):
    ESTADOS = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('DESCATALOGADO', 'Descatalogado'),
    ]
    nombre = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    tipo_identificador = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Elemento"
        verbose_name_plural = "Elementos"

    def __str__(self):
        return self.nombre

class Stock(models.Model):
    elemento = models.ForeignKey(Elemento, on_delete=models.CASCADE, related_name='stocks')
    codigo_is = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='stocks')

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

    def __str__(self):
        return f"{self.nombre} ({self.codigo_is})"

class Cantidad(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cantidades')
    elemento = models.ForeignKey(Elemento, on_delete=models.CASCADE, related_name='cantidades')
    cantidad = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Cantidad"
        verbose_name_plural = "Cantidades"
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'elemento'], name='uq_usuario_elemento')
        ]

    def __str__(self):
        return f"{self.usuario.username} - {self.elemento}: {self.cantidad}"
