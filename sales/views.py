from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.utils import timezone

from oferta.models import Oferta
from .models import Venta, VentaOferta
from users.mixins import GroupVisibilityMixin, SameOwnerRequiredMixin
from mantenimientos.models import Produccion
from utils.ganancia import calcular_ganancia


class VentaListView(GroupVisibilityMixin, ListView):
    model = Venta
    template_name = "sales/ventas_list.html"


class VentaCreateView(GroupVisibilityMixin, CreateView):
    model = Venta
    fields = ['instalacion_numero', 'mantenimiento_numero', 'ppa']   # 👈 NUEVO CAMPO
    template_name = "sales/form.html"
    success_url = reverse_lazy('venta_list')
    extra_context = {"titulo": "Nueva Venta"}

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        venta = form.save()

        # --- Procesar ofertas seleccionadas ---
        ofertas_ids = self.request.POST.getlist("ofertas[]")
        cantidades = self.request.POST.getlist("cantidad[]")

        ganancia_total = 0

        for oferta_id, cantidad in zip(ofertas_ids, cantidades):
            try:
                oferta = Oferta.objects.get(pk=oferta_id)
                cantidad_int = int(cantidad)

                VentaOferta.objects.create(
                    venta=venta,
                    oferta=oferta,
                    cantidad=cantidad_int
                )

                # Ganancia por unidad * cantidad
                ganancia_total += calcular_ganancia(oferta.valor) * cantidad_int

            except Exception as e:
                print(f"Error procesando oferta {oferta_id}: {e}")

        # --- Actualizar Producción mensual ---
        hoy = timezone.now().date()
        obj, created = Produccion.objects.get_or_create(
            usuario=self.request.user,
            año=hoy.year,
            mes=hoy.month,
            defaults={"ganancia_total": ganancia_total}
        )
        if not created:
            obj.ganancia_total += ganancia_total
            obj.save()

        return redirect(self.success_url)


class VentaUpdateView(SameOwnerRequiredMixin, UpdateView):
    model = Venta
    fields = ['instalacion_numero', 'mantenimiento_numero', 'ppa']  # 👈 NUEVO CAMPO
    template_name = "sales/form.html"
    success_url = reverse_lazy('venta_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Editar Venta"
        context["ofertas_existentes"] = self.object.venta_ofertas.select_related("oferta").all()
        return context

    def form_valid(self, form):
        venta = form.save()

        # --- Eliminar ofertas anteriores ---
        venta.venta_ofertas.all().delete()

        # --- Procesar nuevas ofertas ---
        ofertas_ids = self.request.POST.getlist("ofertas[]")
        cantidades = self.request.POST.getlist("cantidad[]")

        ganancia_total = 0

        for oferta_id, cantidad in zip(ofertas_ids, cantidades):
            try:
                oferta = Oferta.objects.get(pk=oferta_id)
                cantidad_int = int(cantidad)

                VentaOferta.objects.create(
                    venta=venta,
                    oferta=oferta,
                    cantidad=cantidad_int
                )

                ganancia_total += calcular_ganancia(oferta.valor) * cantidad_int

            except Exception as e:
                print(f"Error procesando oferta {oferta_id}: {e}")

        # --- Actualizar Producción mensual ---
        hoy = timezone.now().date()
        obj, created = Produccion.objects.get_or_create(
            usuario=self.request.user,
            año=hoy.year,
            mes=hoy.month,
            defaults={"ganancia_total": ganancia_total}
        )
        if not created:
            obj.ganancia_total += ganancia_total
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
