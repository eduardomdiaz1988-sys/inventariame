from django.db import models
from django.contrib.auth.models import User, Group

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    matricula = models.CharField(max_length=50, unique=True)
    grupo_django = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.grupo_django and self.grupo_django.name})"
