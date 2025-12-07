from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class PerfilUsuario(models.Model):
    TIPOS_USUARIO = [
        ("grupo", "Grupo"),
        ("individual", "Individual"),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    tipo_usuario = models.CharField(max_length=10, choices=TIPOS_USUARIO, default="individual")
    matricula = models.CharField(max_length=50, blank=True, null=True)
    nombre_grupo = models.CharField(max_length=100, blank=True, null=True)

    # Relación opcional con el modelo Group de Django
    grupo_django = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario.username} ({self.tipo_usuario})"


# Señal para crear automáticamente el perfil al crear un usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Se crea el perfil con tipo_usuario por defecto ("individual")
        PerfilUsuario.objects.create(usuario=instance)