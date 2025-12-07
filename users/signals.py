from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def crear_grupos(sender, **kwargs):
    for nombre in ["Grupo", "Individual"]:
        Group.objects.get_or_create(name=nombre)
