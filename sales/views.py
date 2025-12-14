# sales/views.py
from decimal import Decimal
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy

from oferta.models import Oferta
from .models import Venta
from users.mixins import GroupVisibilityMixin, SameOwnerRequiredMixin
from referencias.models import Referencia
from django.utils import timezone
from .models import Venta
from mantenimientos.models import Produccion 

class VentaListView(GroupVisibilityMixin, ListView):
    model = Venta
    template_name = "sales/ventas_list.html"


class VentaCreateView(GroupVisibilityMixin, CreateView):
    model = Venta
    fields = ['referencia']
    template_name = "sales/form.html"
    success_url = reverse_lazy('venta_list')
    extra_context = {"titulo": "Nueva Venta"}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['referencia'].queryset = Referencia.objects.all().order_by("nombre")
        form.fields['referencia'].label = "Referencia"
        return form

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        venta = form.save()

        # --- Buscar oferta asociada a la referencia ---
        oferta = Oferta.objects.filter(referencia=venta.referencia).first()
        if oferta:
            try:
                numero = int(oferta.valor.split("+")[1].strip())
            except Exception:
                numero = 0
        else:
            numero = 0

        # --- Calcular ganancia como Decimal ---
        base = Decimal(numero) * Decimal(20)
        ganancia = base * Decimal("0.20")

        # --- Actualizar/crear GananciaMensual ---
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
    fields = ['referencia']
    template_name = "sales/form.html"
    success_url = reverse_lazy('venta_list')
    extra_context = {"titulo": "Editar Venta"}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['referencia'].queryset = Referencia.objects.all().order_by("nombre")
        form.fields['referencia'].label = "Referencia"
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
