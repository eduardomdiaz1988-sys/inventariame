# seed_demo_ofertas.py
from django.core.management.base import BaseCommand
from referencias.models import Referencia
from oferta.models import Oferta

# Mapa de referencias a nombre de oferta y valor
REFERENCIA_INFO = {
    "D1MGX3M": {"nombre": "Magnético", "valor": 3},
    "PT2MX4M": {"nombre": "Magnético", "valor": 4},
    "D1TX3M": {"nombre": "Magnético", "valor": 3},
    "EM1HX5M": {"nombre": "Detector Incendio", "valor": 5},
    "D1HHX3M": {"nombre": "Detector Incendio", "valor": 3},
    "EM15X5M": {"nombre": "Sentinel", "valor": 5},
    "D1PSX3M": {"nombre": "Sentinel", "valor": 3},
    "EM1PX5M": {"nombre": "Pulsador", "valor": 5},
    "D1PSPX3M": {"nombre": "Pulsador", "valor": 3},
    "DIPESN": {"nombre": "MOK", "valor": 5},
    "DIPE5B": {"nombre": "MOK", "valor": 5},
    "DIPE5N": {"nombre": "MOK", "valor": 5},
    "D1ZX7M": {"nombre": "ZeroVision", "valor": 7},
    "D1ZX5M": {"nombre": "ZeroVision", "valor": 5},
    "CVC1X17": {"nombre": "Cámara Arlo Interior", "valor": 7},
    "CVC1X7E": {"nombre": "Cámara Arlo Interior", "valor": 7},
    "CVC1X5": {"nombre": "Cámara Arlo Interior", "valor": 5},
    "CVC1X5E": {"nombre": "Cámara Arlo Interior", "valor": 5},
    "DICERP7M": {"nombre": "Cerradura", "valor": 7},
    "DICERFM": {"nombre": "Cerradura", "valor": 7},
    "PT3MX7M": {"nombre": "Pack Magnético 3 uds", "valor": 7},
    "PT4MX5M": {"nombre": "Pack Magnético 3 uds", "valor": 5},
    "PT4MX7M": {"nombre": "Pack Magnético 5 a 6 uds", "valor": 7},
    "EM2HX7M": {"nombre": "2 Detectores de Incendio", "valor": 7},
    "EM2HX5M": {"nombre": "2 Detectores de Incendio", "valor": 5},
    # Completar con el resto de referencias si lo necesitas
}

class Command(BaseCommand):
    help = "Seed demo de ofertas por cada referencia con nombre y valor"

    def handle(self, *args, **options):
        referencias = Referencia.objects.all()
        for ref in referencias:
            info = REFERENCIA_INFO.get(ref.nombre, None)
            if info:
                nombre_oferta = info["nombre"]
                valor = info["valor"]
            else:
                nombre_oferta = ref.nombre  # fallback si no está en el mapa
                valor = 0

            oferta, created = Oferta.objects.get_or_create(
                nombre=nombre_oferta,
                referencia=ref,
                defaults={"valor": valor}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"Oferta creada: {oferta.nombre} (valor={valor})"
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"Oferta ya existente: {oferta.nombre}"
                ))
