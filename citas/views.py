# Create your views here.
from django.conf import settings
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from django.urls import reverse_lazy

from citas.forms import CitaWithClientForm
from clientes.models import Cliente
from .models import Cita
from users.mixins import LoginRequiredMixin
from locations.models import Address

class CitaListView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = "citas/citas_list.html"
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from citas.models import Cita
from citas.forms import CitaWithClientForm
from clientes.models import Cliente
from locations.models import Address

class CitaCreateWithClientView(LoginRequiredMixin, CreateView):
    model = Cita
    form_class = CitaWithClientForm
    template_name = "citas/card_form/cita_form.html"
    success_url = reverse_lazy('cita_list')
    extra_context = {"titulo": "Nueva Cita"}

    def form_invalid(self, form):
        print("Errores en el formulario:", form.errors)
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        print("POST recibido:", request.POST)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Flujo:
        1. Crear cliente nuevo (si corresponde) o recuperar existente.
        2. Crear dirección principal opcional.
        3. Asignar cliente y usuario a la cita.
        4. Guardar la cita.
        """
        # Valores por defecto
        form.instance.recordatorio = False
        form.instance.estado = "pendiente"

        cliente_id = self.request.POST.get("cliente")
        nombre = self.request.POST.get("nombre", "").strip()
        telefono = self.request.POST.get("telefono", "").strip()
        address = self.request.POST.get("address", "").strip()
        latitude = self.request.POST.get("latitude")
        longitude = self.request.POST.get("longitude")
        label = self.request.POST.get("label", "").strip()

        cliente = None

        # Caso: cliente nuevo
        if not cliente_id and nombre:
            cliente = Cliente.objects.create(
                nombre=nombre,
                telefono=telefono if telefono else None,
                usuario=self.request.user
            )
            # Dirección principal opcional
            if address and latitude and longitude:
                try:
                    direccion_obj = Address.objects.create(
                        user=self.request.user,
                        cliente=cliente,
                        address=address,
                        latitude=float(latitude),
                        longitude=float(longitude),
                        label=label if label else None,
                        principal=True
                    )
                    cliente.direccion = direccion_obj
                    cliente.save()
                except Exception as e:
                    form.add_error(None, f"Error creando dirección: {e}")
                    return self.form_invalid(form)

        # Caso: cliente existente
        elif cliente_id:
            try:
                cliente = Cliente.objects.get(pk=cliente_id)
            except Cliente.DoesNotExist:
                form.add_error("cliente", "El cliente seleccionado no existe")
                return self.form_invalid(form)

        # 🚀 Validación final: aseguramos que siempre haya cliente
        if not cliente:
            form.add_error("cliente", "Debes seleccionar o crear un cliente")
            return self.form_invalid(form)

        # Asignamos cliente y usuario a la cita
        form.instance.cliente = cliente
        form.instance.usuario = self.request.user

        # Guardamos la cita
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
    fields = ['cliente','fecha', 'recordatorio','oferta', 'estado']  # añadido estado
    template_name = "citas/cita_form.html"
    success_url = reverse_lazy('cita_list')
    extra_context = {"titulo": "Editar Cita"}

  
class CitaDeleteView(LoginRequiredMixin, DeleteView):
    model = Cita
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy('cita_list')
    extra_context = {"titulo": "Eliminar Cita"}

class CitaDetailView(DetailView):
    model = Cita
    template_name = "citas/cita_detail.html"
    context_object_name = "cita"