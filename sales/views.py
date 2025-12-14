from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy

from oferta.models import Oferta
from .models import Venta
from users.mixins import GroupVisibilityMixin, SameOwnerRequiredMixin
from django.utils import timezone
from mantenimientos.models import Produccion 
from utils.ganancia import calcular_ganancia  # ✅ función común

class VentaListView(GroupVisibilityMixin, ListView):
    model = Venta
    template_name = "sales/ventas_list.html"


class VentaCreateView(GroupVisibilityMixin, CreateView):
    model = Venta
    fields = ['oferta', 'mantenimiento_numero']   # ✅ añadimos el campo opcional
    template_name = "sales/form.html"
    success_url = reverse_lazy('venta_list')
    extra_context = {"titulo": "Nueva Venta"}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['oferta'].queryset = Oferta.objects.all().order_by("nombre")
        form.fields['oferta'].label = "Oferta"
        form.fields['mantenimiento_numero'].label = "Número de mantenimiento (opcional)"
        return form

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        venta = form.save()

        # --- Usamos directamente la oferta seleccionada ---
        numero = venta.oferta.valor if venta.oferta else 0

        # --- Calcular ganancia usando la función común ---
        ganancia = calcular_ganancia(numero)

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
    fields = ['oferta', 'mantenimiento_numero']   # ✅ también aquí
    template_name = "sales/form.html"
    success_url = reverse_lazy('venta_list')
    extra_context = {"titulo": "Editar Venta"}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['oferta'].queryset = Oferta.objects.all().order_by("nombre")
        form.fields['oferta'].label = "Oferta"
        form.fields['mantenimiento_numero'].label = "Número de mantenimiento (opcional)"
        return form


class VentaDeleteView(SameOwnerRequiredMixin, DeleteView):
    model = Venta
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy('venta_list')
    extra_context = {"titulo": "Eliminar Venta"}


class VentaDetailView(GroupVisibilityMixin, DetailView):
    model = Venta
    template_name = "sales/venta_detail.html"
    context_object_name = "venta"
