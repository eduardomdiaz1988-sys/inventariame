from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import  Cita
from users.mixins import LoginRequiredMixin



class CitaListView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = "core/citas_list.html"

class CitaCreateView(LoginRequiredMixin, CreateView):
    model = Cita
    fields = ['cliente', 'direccion', 'fecha', 'recordatorio']
    template_name = "core/form.html"
    success_url = reverse_lazy('cita_list')
    extra_context = {"titulo": "Nueva Cita"}

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class CitaUpdateView(LoginRequiredMixin, UpdateView):
    model = Cita
    fields = ['cliente', 'direccion', 'fecha', 'recordatorio', 'venta']
    template_name = "core/form.html"
    success_url = reverse_lazy('cita_list')
    extra_context = {"titulo": "Editar Cita"}

class CitaDeleteView(LoginRequiredMixin, DeleteView):
    model = Cita
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy('cita_list')
    extra_context = {"titulo": "Eliminar Cita"}
