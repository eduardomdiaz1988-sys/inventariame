# sales/migrations/000X_copy_old_ventas.py
from django.db import migrations

def copy_old_ventas(apps, schema_editor):
    Venta = apps.get_model("sales", "Venta")
    VentaOferta = apps.get_model("sales", "VentaOferta")
    Oferta = apps.get_model("oferta", "Oferta")

    # si aún existen columnas antiguas en la BD de Heroku
    for venta in Venta.objects.all():
        if hasattr(venta, "oferta_id") and venta.oferta_id:
            try:
                VentaOferta.objects.create(
                    venta=venta,
                    oferta_id=venta.oferta_id,
                    cantidad=getattr(venta, "cantidad", 1)
                )
            except Exception as e:
                print(f"Error migrando venta {venta.id}: {e}")

class Migration(migrations.Migration):
    dependencies = [
        ("sales", "000X_last"),  # ajusta al último número
    ]
    operations = [
        migrations.RunPython(copy_old_ventas),
    ]
