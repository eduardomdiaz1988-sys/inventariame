from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy

from oferta.models import Oferta
from .models import Venta, VentaOferta
from users.mixins import GroupVisibilityMixin, SameOwnerRequiredMixin
from django.utils import timezone
from mantenimientos.models import Produccion 
from utils.ganancia import calcular_ganancia  # ✅ función común


class VentaListView(GroupVisibilityMixin, ListView):
    model = Venta
    template_name = "sales/ventas_list.html"


class VentaCreateView(GroupVisibilityMixin, CreateView):
    model = Venta
    fields = ['mantenimiento_numero', 'ppa']   # ✅ ya no incluimos 'oferta' directamente
    template_name = "sales/form.html"
    success_url = reverse_lazy('venta_list')
    extra_context = {"titulo": "Nueva Venta"}

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        venta = form.save()

        # --- Procesar las ofertas seleccionadas desde el formulario ---
        ofertas_ids = self.request.POST.getlist("ofertas[]")
        cantidades = self.request.POST.getlist("cantidad[]")

        total_valor = 0
        for oferta_id, cantidad in zip(ofertas_ids, cantidades):
            try:
                oferta = Oferta.objects.get(pk=oferta_id)
                cantidad_int = int(cantidad)
                # Crear relación en VentaOferta
                VentaOferta.objects.create(
                    venta=venta,
                    oferta=oferta,
                    cantidad=cantidad_int
                )
                total_valor += oferta.valor * cantidad_int
            except Exception as e:
                print(f"Error procesando oferta {oferta_id}: {e}")

        # --- Calcular ganancia usando la función común ---
        ganancia = calcular_ganancia(total_valor)

        # --- Actualizar/crear Producción mensual ---
        hoy = timezone.now().date()
        obj, created = Produccion.objects.get_or_create(
            usuario=self.request.user,
            año=hoy.year,
            mes=hoy.month,
            defaults={"ganancia_total": ganancia}
        )
        if not created:
            obj.ganancia_total += ganancia
            obj.save()

        return redirect(self.success_url)


class VentaUpdateView(SameOwnerRequiredMixin, UpdateView):
    model = Venta
    fields = ['mantenimiento_numero', 'ppa']
    template_name = "sales/form.html"
    success_url = reverse_lazy('venta_list')
    extra_context = {"titulo": "Editar Venta"}

    def form_valid(self, form):
        venta = form.save()

        # --- Limpiar ofertas anteriores ---
        venta.venta_ofertas.all().delete()

        # --- Procesar nuevas ofertas ---
        ofertas_ids = self.request.POST.getlist("ofertas[]")
        cantidades = self.request.POST.getlist("cantidad[]")

        total_valor = 0
        for oferta_id, cantidad in zip(ofertas_ids, cantidades):
            try:
                oferta = Oferta.objects.get(pk=oferta_id)
                cantidad_int = int(cantidad)
                VentaOferta.objects.create(
                    venta=venta,
                    oferta=oferta,
                    cantidad=cantidad_int
                )
                total_valor += oferta.valor * cantidad_int
            except Exception as e:
                print(f"Error procesando oferta {oferta_id}: {e}")

        # --- Recalcular ganancia ---
        ganancia = calcular_ganancia(total_valor)
        hoy = timezone.now().date()
        obj, created = Produccion.objects.get_or_create(
            usuario=self.request.user,
            año=hoy.year,
            mes=hoy.month,
            defaults={"ganancia_total": ganancia}
        )
        if not created:
            obj.ganancia_total += ganancia
            obj.save()

        return redirect(self.success_url)


class VentaDeleteView(SameOwnerRequiredMixin, DeleteView):
    model = Venta
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy('venta_list')
    extra_context = {"titulo": "Eliminar Venta"}


class VentaDetailView(GroupVisibilityMixin, DetailView):
    model = Venta
    template_name = "sales/venta_detail.html"
    context_object_name = "venta"
