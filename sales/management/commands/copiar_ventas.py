from django.core.management.base import BaseCommand
from sales.models import Venta, VentaOferta

class Command(BaseCommand):
    help = "Copiar datos antiguos de Venta.oferta y cantidad a VentaOferta"

    def handle(self, *args, **options):
        for venta in Venta.objects.all():
            if hasattr(venta, "oferta_id") and venta.oferta_id:
                cantidad = getattr(venta, "cantidad", 1)
                try:
                    VentaOferta.objects.create(
                        venta=venta,
                        oferta_id=venta.oferta_id,
                        cantidad=cantidad
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f"Copiada oferta {venta.oferta_id} en venta {venta.id}"
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"Error en venta {venta.id}: {e}"
                    ))
