from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from users.models import PerfilUsuario
from core.models import Cliente, Cita
from sales.models import Venta
from inventory.models import Elemento, Cantidad
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "Crea grupos, usuarios de prueba, perfiles y datos demo para Inventariame"

    def handle(self, *args, **options):
        # Crear grupos principales
        grupo, _ = Group.objects.get_or_create(name="Grupo")
        individual, _ = Group.objects.get_or_create(name="Individual")

        # Crear usuarios de prueba
        u1, _ = User.objects.get_or_create(username="orbe", email="orbe@example.com")
        u1.set_password("Demo1234"); u1.save()
        PerfilUsuario.objects.get_or_create(
            usuario=u1,
            tipo_usuario="grupo",
            matricula="GRP001",
            nombre_grupo="Equipo Orbe",
            grupo_django=grupo
        )

        u2, _ = User.objects.get_or_create(username="maria", email="maria@example.com")
        u2.set_password("Demo1234"); u2.save()
        PerfilUsuario.objects.get_or_create(
            usuario=u2,
            tipo_usuario="individual",
            matricula="IND001",
            grupo_django=individual
        )

        u3, _ = User.objects.get_or_create(username="jefe", email="jefe@example.com")
        u3.set_password("Demo1234"); u3.save()
        PerfilUsuario.objects.get_or_create(
            usuario=u3,
            tipo_usuario="grupo",
            matricula="GRP002",
            nombre_grupo="Equipo Jefe",
            grupo_django=grupo
        )

        # Crear clientes vinculados a usuarios
        c1, _ = Cliente.objects.get_or_create(nombre="Juan Pérez", usuario=u1)
        c2, _ = Cliente.objects.get_or_create(nombre="Marina López", usuario=u2)
        c3, _ = Cliente.objects.get_or_create(nombre="Carlos Sánchez", usuario=u1)

        # Crear citas vinculadas a usuarios
        Cita.objects.get_or_create(cliente=c1, usuario=u1, fecha=timezone.now()+timedelta(days=1), recordatorio=True)
        Cita.objects.get_or_create(cliente=c2, usuario=u2, fecha=timezone.now()+timedelta(days=3), recordatorio=False)

        # Crear ventas vinculadas a usuarios
        Venta.objects.get_or_create(referencia="V001", precio=100, instalacion=2, mantenimiento=1, usuario=u1, cliente=c1)
        Venta.objects.get_or_create(referencia="V002", precio=250, instalacion=1, mantenimiento=0, usuario=u2, cliente=c2)

        # Crear elementos vinculados a usuarios
        e1, _ = Elemento.objects.get_or_create(nombre="Magnetico", estado="BUENO", tipo_identificador="HW", usuario=u1)
        e2, _ = Elemento.objects.get_or_create(nombre="Fotodetector", estado="BUENO", tipo_identificador="HW", usuario=u1)
        e3, _ = Elemento.objects.get_or_create(nombre="Panel Central", estado="DEFECTUOSO", tipo_identificador="HW", usuario=u2)

        # Crear cantidades vinculadas a usuarios
        Cantidad.objects.get_or_create(usuario=u1, elemento=e1, cantidad=5)
        Cantidad.objects.get_or_create(usuario=u1, elemento=e2, cantidad=1)
        Cantidad.objects.get_or_create(usuario=u2, elemento=e3, cantidad=0)

        self.stdout.write(self.style.SUCCESS("Datos demo creados con éxito"))
