from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
from django.contrib.auth.models import User, Group

from clientes.models import Cliente
from locations.models import Address
from citas.models import Cita
from oferta.models import Oferta
from referencias.models import Referencia, Tipo
from sales.models import Venta
from inventory.models import Elemento, Stock, Cantidad
from users.models import PerfilUsuario
from mantenimientos.models import Mantenimiento, ConfiguracionMantenimientos


class Command(BaseCommand):
    help = "Carga datos de demo completos en la base de datos"

    def handle(self, *args, **options):
        # --- Grupos ---
        grupo_group, _ = Group.objects.get_or_create(name="Grupo")
        Group.objects.get_or_create(name="Individual")

        # --- Usuarios demo ---
        admin, _ = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True}
        )

        # --- Contraseñas demo ---
        admin.set_password("Demo1234")

        admin.save()


        # --- Perfiles ---
        def ensure_profile(user, group_obj, tipo_usuario, nombre_grupo):
            user.groups.add(group_obj)
            perfil, created = PerfilUsuario.objects.get_or_create(
                usuario=user,
                defaults={
                    "tipo_usuario": tipo_usuario,
                    "matricula": f"MAT-{user.username.upper()}",
                    "nombre_grupo": nombre_grupo,
                    "creado": timezone.now(),
                    "actualizado": timezone.now(),
                    "grupo_django": group_obj
                }
            )
            if not created:
                perfil.tipo_usuario = tipo_usuario
                perfil.nombre_grupo = nombre_grupo
                perfil.grupo_django = group_obj
                perfil.actualizado = timezone.now()
                perfil.save()

        ensure_profile(admin, grupo_group, "Grupo", "Admin")
        

        # --- Tipos y referencias ---
        Tipo.objects.get_or_create(nombre="Fast")
        Tipo.objects.get_or_create(nombre="Moonshot")

  
        self.stdout.write(self.style.SUCCESS(
            "Seed demo completado: usuarios, perfiles, clientes, direcciones, ventas, citas, inventario y mantenimientos."
        ))
