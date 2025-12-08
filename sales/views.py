from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Venta
from users.mixins import GroupVisibilityMixin, SameOwnerRequiredMixin
from referencias.models import Referencia


class VentaListView(GroupVisibilityMixin, ListView):
    model = Venta
    template_name = "sales/ventas_list.html"

class VentaCreateView(GroupVisibilityMixin, CreateView):
    model = Venta
    fields = ['referencia', 'precio', 'instalacion', 'mantenimiento', 'cliente']
    template_name = "sales/form.html"
    success_url = reverse_lazy('venta_list')
    extra_context = {"titulo": "Nueva Venta"}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Aseguramos que el campo referencia se muestre como un select con todas las referencias
        form.fields['referencia'].queryset = Referencia.objects.all().order_by("nombre")
        form.fields['referencia'].label = "Referencia"
        return form

    def form_valid(self, form):
        # Asignamos el usuario actual a la venta
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class VentaUpdateView(SameOwnerRequiredMixin, UpdateView):
    model = Venta
    fields = ['referencia', 'precio', 'instalacion', 'mantenimiento', 'cliente']
    template_name = "sales/form.html"
    success_url = reverse_lazy('venta_list')
    extra_context = {"titulo": "Editar Venta"}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Mostrar todas las referencias en el select
        form.fields['referencia'].queryset = Referencia.objects.all().order_by("nombre")
        form.fields['referencia'].label = "Referencia"
        return form
    

class VentaDeleteView(SameOwnerRequiredMixin, DeleteView):
    model = Venta
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy('venta_list')
    extra_context = {"titulo": "Eliminar Venta"}
