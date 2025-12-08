from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User, Group

from clientes.models import Cliente
from locations.models import Address
from citas.models import Cita
from oferta.models import Oferta
from referencias.models import Referencia, Tipo
from sales.models import Venta
from inventory.models import Elemento, Stock, Cantidad
from users.models import PerfilUsuario

class Command(BaseCommand):
    help = "Carga datos de demo completos en la base de datos"

    def handle(self, *args, **options):
        # --- Grupos ---
        grupo_group, _ = Group.objects.get_or_create(name="Grupo")
        individual_group, _ = Group.objects.get_or_create(name="Individual")

        # --- Usuarios demo ---
        admin, _ = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True}
        )
        user1, _ = User.objects.get_or_create(username="eduardo", defaults={"email": "eduardo@example.com"})
        user2, _ = User.objects.get_or_create(username="maria", defaults={"email": "maria@example.com"})

        # --- Contraseñas demo ---
        admin.set_password("admin123")
        user1.set_password("eduardo123")
        user2.set_password("maria123")
        admin.save()
        user1.save()
        user2.save()

        # --- Perfiles ---
        def ensure_profile(user, group_obj, tipo_usuario, nombre_grupo):
            user.groups.add(group_obj)
            perfil, created = PerfilUsuario.objects.get_or_create(
                usuario=user,
                defaults={
                    "tipo_usuario": tipo_usuario,
                    "matricula": f"MAT-{user.username.upper()}",
                    "nombre_grupo": nombre_grupo,
                    "creado": timezone.now(),
                    "actualizado": timezone.now(),
                    "grupo_django": group_obj
                }
            )
            if not created:
                perfil.tipo_usuario = tipo_usuario
                perfil.nombre_grupo = nombre_grupo
                perfil.grupo_django = group_obj
                perfil.actualizado = timezone.now()
                perfil.save()

        ensure_profile(admin, grupo_group, "Grupo", "Administradores")
        ensure_profile(user1, individual_group, "Individual", "Comerciales")
        ensure_profile(user2, grupo_group, "Grupo", "Operaciones")

        # --- Tipos y referencias ---
        tipo_servicio, _ = Tipo.objects.get_or_create(nombre="Servicio")
        tipo_producto, _ = Tipo.objects.get_or_create(nombre="Producto")

        ref1, _ = Referencia.objects.get_or_create(nombre="Panel Solar", tipo=tipo_producto)
        ref2, _ = Referencia.objects.get_or_create(nombre="Mantenimiento anual", tipo=tipo_servicio)

        # --- Ofertas ---
        oferta1, _ = Oferta.objects.get_or_create(nombre="Oferta Solar Básica", referencia=ref1, tipo=tipo_producto, valor="10%")
        oferta2, _ = Oferta.objects.get_or_create(nombre="Pack Mantenimiento", referencia=ref2, tipo=tipo_servicio, valor="Gratis primer año")

        # --- Clientes ---
        cliente1, _ = Cliente.objects.get_or_create(nombre="Cliente Uno", telefono="600111222", usuario=user1)
        cliente2, _ = Cliente.objects.get_or_create(nombre="Cliente Dos", telefono="600333444", usuario=user2)

        # --- Direcciones ---
        addr1, _ = Address.objects.get_or_create(
            label="Casa Cliente Uno",
            address="Calle Mayor 1, Málaga",
            latitude=36.7213,
            longitude=-4.4214,
            user=user1,
            cliente=cliente1,
            defaults={"created_at": timezone.now()}
        )
        addr2, _ = Address.objects.get_or_create(
            label="Oficina Cliente Dos",
            address="Av. Andalucía 25, Sevilla",
            latitude=37.3891,
            longitude=-5.9845,
            user=user2,
            cliente=cliente2,
            defaults={"created_at": timezone.now()}
        )

        if not cliente1.direccion:
            cliente1.direccion = addr1
            cliente1.save(update_fields=["direccion"])
        if not cliente2.direccion:
            cliente2.direccion = addr2
            cliente2.save(update_fields=["direccion"])

        # --- Ventas ---
        venta1, _ = Venta.objects.get_or_create(
            cliente=cliente1,
            usuario=user1,
            referencia=ref1,
            defaults={"precio": 1200, "instalacion": 200, "mantenimiento": 100}
        )
        venta2, _ = Venta.objects.get_or_create(
            cliente=cliente2,
            usuario=user2,
            referencia=ref2,
            defaults={"precio": 500, "instalacion": 50, "mantenimiento": 50}
        )

        # --- Citas ---
        estados = ["pendiente", "confirmada", "cancelada"]
        for i in range(6):
            fecha = timezone.now() + timedelta(days=i + 1, hours=9)
            Cita.objects.get_or_create(
                cliente=cliente1 if i % 2 == 0 else cliente2,
                usuario=user1 if i % 2 == 0 else user2,
                direccion=addr1 if i % 2 == 0 else addr2,
                fecha=fecha,
                recordatorio=(i % 2 == 0),
                estado=estados[i % len(estados)],
                oferta=oferta1 if i % 2 == 0 else oferta2,
                venta=venta1 if i % 2 == 0 else venta2
            )

        # --- Inventario ---
        elem1, _ = Elemento.objects.get_or_create(nombre="Inversor Solar", estado="nuevo", tipo_identificador="INV-001", usuario=user1)
        elem2, _ = Elemento.objects.get_or_create(nombre="Batería", estado="usado", tipo_identificador="BAT-002", usuario=user2)

        Stock.objects.get_or_create(codigo_is="STK001", nombre="Stock Inversores", elemento=elem1, usuario=user1)
        Stock.objects.get_or_create(codigo_is="STK002", nombre="Stock Baterías", elemento=elem2, usuario=user2)

        Cantidad.objects.get_or_create(usuario=user1, elemento=elem1, defaults={"cantidad": 10})
        Cantidad.objects.get_or_create(usuario=user2, elemento=elem2, defaults={"cantidad": 5})

        self.stdout.write(self.style.SUCCESS("Seed demo completado con contraseñas definidas, grupos, perfiles, usuarios, clientes, direcciones, citas, ofertas, ventas e inventario."))
