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

    

        # --- Tipos y referencias ---
        Tipo.objects.get_or_create(nombre="Fast")
        Tipo.objects.get_or_create(nombre="Moonshot")

  
        self.stdout.write(self.style.SUCCESS(
            "Seed demo completado: usuarios, perfiles, clientes, direcciones, ventas, citas, inventario y mantenimientos."
        ))
