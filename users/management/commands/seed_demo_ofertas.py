# seed_demo_ofertas.py
from django.core.management.base import BaseCommand
from referencias.models import Referencia
from oferta.models import Oferta
import random

VALORES_PERMITIDOS = [3, 4, 5, 7, 10]

class Command(BaseCommand):
    help = "Seed demo de ofertas por cada referencia"

    def handle(self, *args, **options):
        referencias = Referencia.objects.all()
        for ref in referencias:
            nombre_oferta = f"Oferta {ref.nombre}"
            valor = random.choice(VALORES_PERMITIDOS)
            oferta, created = Oferta.objects.get_or_create(
                nombre=nombre_oferta,
                referencia=ref,
                defaults={"valor": valor}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Oferta creada: {oferta.nombre} (valor=0 + {valor})"))
            else:
                self.stdout.write(self.style.WARNING(f"Oferta ya existente: {oferta.nombre}"))
