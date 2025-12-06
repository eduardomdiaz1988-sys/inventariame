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
        # Crear grupos
        empresa, _ = Group.objects.get_or_create(name="Empresa")
        particular, _ = Group.objects.get_or_create(name="Particular")
        jefe, _ = Group.objects.get_or_create(name="JefeEquipo")

        # Crear usuarios
        u1, _ = User.objects.get_or_create(username="orbe", email="orbe@example.com")
        u1.set_password("demo1234"); u1.save()
        PerfilUsuario.objects.get_or_create(user=u1, matricula="EMP001", grupo_django=empresa)

        u2, _ = User.objects.get_or_create(username="maria", email="maria@example.com")
        u2.set_password("demo1234"); u2.save()
        PerfilUsuario.objects.get_or_create(user=u2, matricula="PAR001", grupo_django=particular)

        u3, _ = User.objects.get_or_create(username="jefe", email="jefe@example.com")
        u3.set_password("demo1234"); u3.save()
        PerfilUsuario.objects.get_or_create(user=u3, matricula="JEF001", grupo_django=jefe)

        # Crear clientes
        c1, _ = Cliente.objects.get_or_create(nombre="Juan Pérez")
        c2, _ = Cliente.objects.get_or_create(nombre="Marina López")
        c3, _ = Cliente.objects.get_or_create(nombre="Carlos Sánchez")

        # Crear citas
        Cita.objects.get_or_create(cliente=c1, usuario=u1, fecha=timezone.now()+timedelta(days=1), recordatorio=True)
        Cita.objects.get_or_create(cliente=c2, usuario=u2, fecha=timezone.now()+timedelta(days=3), recordatorio=False)

        # Crear ventas
        Venta.objects.get_or_create(referencia="V001", precio=100, instalacion=2, mantenimiento=1, usuario=u1, cliente=c1)
        Venta.objects.get_or_create(referencia="V002", precio=250, instalacion=1, mantenimiento=0, usuario=u2, cliente=c2)

        # Crear elementos
        e1, _ = Elemento.objects.get_or_create(nombre="Router", estado="ACTIVO", tipo_identificador="HW")
        e2, _ = Elemento.objects.get_or_create(nombre="Switch", estado="ACTIVO", tipo_identificador="HW")
        e3, _ = Elemento.objects.get_or_create(nombre="Cable", estado="INACTIVO", tipo_identificador="HW")

        # Crear cantidades
        Cantidad.objects.get_or_create(usuario=u1, elemento=e1, cantidad=5)
        Cantidad.objects.get_or_create(usuario=u1, elemento=e2, cantidad=1)
        Cantidad.objects.get_or_create(usuario=u2, elemento=e3, cantidad=0)

        self.stdout.write(self.style.SUCCESS("Datos demo creados con éxito"))
