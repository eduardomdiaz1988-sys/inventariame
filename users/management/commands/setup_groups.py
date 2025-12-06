from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from inventory.models import Elemento, Stock
from core.models import Cita, Cliente
from sales.models import Venta

class Command(BaseCommand):
    help = "Crea grupos Empresa y Particular y asigna permisos base"

    def handle(self, *args, **options):
        empresa, _ = Group.objects.get_or_create(name='Empresa')
        particular, _ = Group.objects.get_or_create(name='Particular')
        jefes, _ = Group.objects.get_or_create(name='JefeEquipo')

        # Permisos para jefes: pueden añadir Elementos y Stocks
        ct_elemento = ContentType.objects.get_for_model(Elemento)
        ct_stock = ContentType.objects.get_for_model(Stock)
        can_add_elemento = Permission.objects.get(codename='add_elemento', content_type=ct_elemento)
        can_add_stock = Permission.objects.get(codename='add_stock', content_type=ct_stock)

        jefes.permissions.add(can_add_elemento, can_add_stock)

        self.stdout.write(self.style.SUCCESS("Grupos y permisos configurados"))
