from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Venta
from users.mixins import GroupVisibilityMixin, SameOwnerRequiredMixin

class VentaListView(GroupVisibilityMixin, ListView):
    model = Venta
    template_name = "sales/ventas_list.html"

class VentaCreateView(GroupVisibilityMixin, CreateView):
    model = Venta
    fields = ['referencia', 'precio', 'instalacion', 'mantenimiento', 'cliente']
    template_name = "core/form.html"
    success_url = reverse_lazy('venta_list')
    extra_context = {"titulo": "Nueva Venta"}

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class VentaUpdateView(SameOwnerRequiredMixin, UpdateView):
    model = Venta
    fields = ['referencia', 'precio', 'instalacion', 'mantenimiento', 'cliente']
    template_name = "core/form.html"
    success_url = reverse_lazy('venta_list')
    extra_context = {"titulo": "Editar Venta"}

class VentaDeleteView(SameOwnerRequiredMixin, DeleteView):
    model = Venta
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy('venta_list')
    extra_context = {"titulo": "Eliminar Venta"}
