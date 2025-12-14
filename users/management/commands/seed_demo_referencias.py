# referencias/management/commands/seed_demo_referencias.py
from django.core.management.base import BaseCommand
from referencias.models import Referencia, Tipo

def calcular_ganancia(valor):
    if valor == 3 or valor == 4:
        return 12
    elif valor == 5:
        return 20
    elif valor == 7:
        return 28
    elif valor == 10:
        return 40
    return None

REFERENCIAS = [
    {"nombre": "D1MGX3M", "tipo": 1, "valor": 3},
    {"nombre": "PT2MX4M", "tipo": 1, "valor": 4},
    {"nombre": "D1TX3M", "tipo": 1, "valor": 3},
    {"nombre": "EM1HX5M", "tipo": 1, "valor": 5},
    {"nombre": "D1HHX3M", "tipo": 1, "valor": 5},
    {"nombre": "EM15X5M", "tipo": 1, "valor": 5},
    {"nombre": "D1PSX3M", "tipo": 1, "valor": 3},
    {"nombre": "EM1PX5M", "tipo": 1, "valor": 5},
    {"nombre": "D1PSPX3M", "tipo": 1, "valor": 3},
    {"nombre": "DIPESN", "tipo": 1, "valor": 5},
    {"nombre": "DIPE5B", "tipo": 1, "valor": 5},
    {"nombre": "DIPE5N", "tipo": 1, "valor": 5},
    {"nombre": "D1ZX7M", "tipo": 1, "valor": 7},
    {"nombre": "D1ZX5M", "tipo": 1, "valor": 5},
    {"nombre": "CVC1X17", "tipo": 1, "valor": 7},
    {"nombre": "CVC1X7E", "tipo": 1, "valor": 7},
    {"nombre": "CVC1X5", "tipo": 1, "valor": 5},
    {"nombre": "CVC1X5E", "tipo": 1, "valor": 5},
    {"nombre": "DICERP7M", "tipo": 1, "valor": 7},
    {"nombre": "DICERFM", "tipo": 1, "valor": 7},
    {"nombre": "PT3MX7M", "tipo": 1, "valor": 7},
    {"nombre": "PT4MX5M", "tipo": 1, "valor": 5},
    {"nombre": "PT4MX7M", "tipo": 1, "valor": 7},
    {"nombre": "EM2HX7M", "tipo": 1, "valor": 7},
    {"nombre": "EM2HX5M", "tipo": 1, "valor": 5},
    {"nombre": "D1IF2503", "tipo": 0, "valor": 3},
    {"nombre": "D1IF2523", "tipo": 0, "valor": 3},
    {"nombre": "P24F252", "tipo": 0, "valor": 4},
    {"nombre": "P24F250", "tipo": 0, "valor": 4},
    {"nombre": "EM1HX5F", "tipo": 0, "valor": 5},
    {"nombre": "D1IHX3F", "tipo": 0, "valor": 3},
    {"nombre": "EM1SX5F", "tipo": 0, "valor": 5},
    {"nombre": "D1ISX3M", "tipo": 1, "valor": 3},
    {"nombre": "EM1PX5F", "tipo": 0, "valor": 5},
    {"nombre": "D1IPX3F", "tipo": 0, "valor": 3},
    {"nombre": "D1ZVX7F", "tipo": 0, "valor": 7},
    {"nombre": "D1ZVX5F", "tipo": 0, "valor": 5},
    {"nombre": "P1IFX7F", "tipo": 0, "valor": 7},
    {"nombre": "P1IFX5F", "tipo": 0, "valor": 5},
    {"nombre": "CV1ICX7", "tipo": 0, "valor": 7},
    {"nombre": "CV1ICX7NE", "tipo": 0, "valor": 7},
    {"nombre": "CV1ICX5", "tipo": 0, "valor": 5},
    {"nombre": "CV1ICX5NE", "tipo": 0, "valor": 5},
    {"nombre": "CV1ECX7", "tipo": 0, "valor": 7},
    {"nombre": "CV1ECX7NE", "tipo": 0, "valor": 7},
    {"nombre": "CV1ECX5", "tipo": 0, "valor": 5},
    {"nombre": "CV1ECX5NE", "tipo": 0, "valor": 5},
    {"nombre": "D1CERR7F", "tipo": 0, "valor": 7},
    {"nombre": "D1CERR5F", "tipo": 0, "valor": 5},
    {"nombre": "P1IPX7F", "tipo": 0, "valor": 7},
    {"nombre": "P1IPX5F", "tipo": 0, "valor": 5},
    {"nombre": "OV5SX4F7", "tipo": 0, "valor": 7},
    {"nombre": "OV5SX4C5", "tipo": 0, "valor": 5},
    {"nombre": "P3F7F252", "tipo": 0, "valor": 7},
    {"nombre": "P3F7F250", "tipo": 0, "valor": 7},
    {"nombre": "P3F5F252", "tipo": 0, "valor": 5},
    {"nombre": "P3F5F250", "tipo": 0, "valor": 5},
    {"nombre": "P4F7F252", "tipo": 0, "valor": 7},
    {"nombre": "P4F7F250", "tipo": 0, "valor": 7},
    {"nombre": "P4F5F252", "tipo": 0, "valor": 5},
    {"nombre": "P4F5F250", "tipo": 0, "valor": 5},
    {"nombre": "EM2HX7F", "tipo": 0, "valor": 7},
    {"nombre": "EM2HX5F", "tipo": 0, "valor": 5},
    {"nombre": "F4A3", "tipo": 0, "valor": 0},
    {"nombre": "F4A9", "tipo": 0, "valor": 0},
    {"nombre": "2409SP", "tipo": 0, "valor": 0},
    {"nombre": "2411SP", "tipo": 0, "valor": 0},
]

class Command(BaseCommand):
    help = "Seed referencias demo en la base de datos con ganancia"

    def handle(self, *args, **options):
        # Creamos tipos si no existen
        fast, _ = Tipo.objects.get_or_create(id=0, defaults={"nombre": "Fast"})
        moonshoot, _ = Tipo.objects.get_or_create(id=1, defaults={"nombre": "Moonshoot"})

        for ref in REFERENCIAS:
            tipo_obj = fast if ref["tipo"] == 0 else moonshoot
            ganancia = calcular_ganancia(ref["valor"])
            obj, created = Referencia.objects.update_or_create(
                nombre=ref["nombre"],
                defaults={
                    "tipo": tipo_obj,
                    "valor": ref["valor"],
                    "ganancia": ganancia,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"Referencia creada: {obj.nombre} (valor={obj.valor}, ganancia={obj.ganancia})"
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"Referencia actualizada: {obj.nombre} (valor={obj.valor}, ganancia={obj.ganancia})"
                ))
