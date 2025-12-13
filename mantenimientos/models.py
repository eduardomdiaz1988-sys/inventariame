from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Mantenimiento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mantenimientos")
    fecha = models.DateField()
    cantidad = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"
        ordering = ["-fecha"]
        constraints = [
            models.UniqueConstraint(fields=["usuario", "fecha"], name="unique_mantenimiento_usuario_fecha"),
        ]

    def __str__(self):
        return f"{self.usuario} → {self.fecha} → {self.cantidad}"

    def clean(self):
        # Validar presencia de usuario para que el resto de reglas funcionen bien
        if not self.usuario_id:
            raise ValidationError({"usuario": "No se ha podido asociar el usuario al mantenimiento."})

        # Rango de cantidad
        if self.cantidad < 0:
            raise ValidationError({"cantidad": "La cantidad no puede ser menor que 0."})
        if self.cantidad > 15:
            raise ValidationError({"cantidad": "La cantidad no puede ser mayor que 15."})

        # Duplicados usuario+fecha (evita colisión al editar fecha)
        qs = Mantenimiento.objects.filter(usuario=self.usuario, fecha=self.fecha)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError({"fecha": "Ya existe un mantenimiento para este usuario en esa fecha."})
