from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Address(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="addresses",
        null=True,
        blank=True
    )
    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="direcciones"
    )
    label = models.CharField(max_length=120, blank=True, null=True)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()   # ✅ más cómodo para Google Maps
    longitude = models.FloatField()
    principal = models.BooleanField(default=False)  # ✅ nuevo campo
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.label or 'Dirección'}: {self.address}"
