from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from users.models import PerfilUsuario
from core.models import Cliente, Cita
from sales.models import Venta
from inventory.models import Elemento, Cantidad

class Command(BaseCommand):
    help = "Elimina todos los datos demo creados por seed_demo"

    def handle(self, *args, **options):
        # Borrar datos en orden seguro
        self.stdout.write("Eliminando citas...")
        Cita.objects.all().delete()

        self.stdout.write("Eliminando ventas...")
        Venta.objects.all().delete()

        self.stdout.write("Eliminando cantidades...")
        Cantidad.objects.all().delete()

        self.stdout.write("Eliminando elementos...")
        Elemento.objects.all().delete()

        self.stdout.write("Eliminando clientes...")
        Cliente.objects.all().delete()

        self.stdout.write("Eliminando perfiles...")
        PerfilUsuario.objects.all().delete()

        self.stdout.write("Eliminando usuarios demo...")
        User.objects.filter(username__in=["orbe", "maria", "jefe"]).delete()

        self.stdout.write("Eliminando grupos demo...")
        Group.objects.filter(name__in=["Empresa", "Particular", "JefeEquipo"]).delete()

        self.stdout.write(self.style.SUCCESS("Datos demo eliminados con éxito"))
