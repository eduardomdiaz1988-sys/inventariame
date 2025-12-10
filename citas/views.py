# Create your views here.
from django.conf import settings
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from citas.forms import CitaWithClientForm
from clientes.models import Cliente
from .models import Cita
from users.mixins import LoginRequiredMixin
from locations.models import Address

class CitaListView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = "citas/citas_list.html"

class CitaCreateWithClientView(LoginRequiredMixin, CreateView):
    model = Cita
    form_class = CitaWithClientForm
    template_name = "citas/card_form/cita_form.html"
    success_url = reverse_lazy('cita_list')
    extra_context = {"titulo": "Nueva Cita"}

    def form_valid(self, form):
        """
        Si el cliente es nuevo, lo creamos junto con su dirección principal
        antes de guardar la cita.
        """
        cliente_id = self.request.POST.get("cliente")
        nombre = self.request.POST.get("nombre")
        telefono = self.request.POST.get("telefono")
        address = self.request.POST.get("address")
        latitude = self.request.POST.get("latitude")
        longitude = self.request.POST.get("longitude")
        label = self.request.POST.get("label")

        # Si no hay cliente_id pero sí datos de cliente nuevo → creamos cliente
        if not cliente_id and nombre:
            cliente = Cliente.objects.create(
                nombre=nombre,
                telefono=telefono,
                usuario=self.request.user
            )
            if address and latitude and longitude:
                Address.objects.create(
                    cliente=cliente,
                    address=address,
                    latitude=latitude,
                    longitude=longitude,
                    label=label if label else None,
                    principal=True
                )
            form.instance.cliente = cliente
        else:
            # cliente existente
            form.instance.cliente_id = cliente_id

        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # añadimos la API Key de Google Maps al contexto
        context["GOOGLE_MAPS_API_KEY"] = settings.GOOGLE_MAPS_API_KEY
        return context
    
class CitaCreateView(LoginRequiredMixin, CreateView):
    model = Cita
    fields = ['cliente','fecha', 'recordatorio', 'oferta', 'estado']  # añadido estado
    template_name = "citas/cita_form.html"
    success_url = reverse_lazy('cita_list')
    extra_context = {"titulo": "Nueva Cita"}

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class CitaUpdateView(LoginRequiredMixin, UpdateView):
    model = Cita
    fields = ['cliente','fecha', 'recordatorio', 'venta', 'oferta', 'estado']  # añadido estado
    template_name = "citas/cita_form.html"
    success_url = reverse_lazy('cita_list')
    extra_context = {"titulo": "Editar Cita"}

  
class CitaDeleteView(LoginRequiredMixin, DeleteView):
    model = Cita
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy('cita_list')
    extra_context = {"titulo": "Eliminar Cita"}
