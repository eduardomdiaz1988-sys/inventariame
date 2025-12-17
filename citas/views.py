from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from citas.forms import CitaWithClientForm
from clientes.models import Cliente
from locations.models import Address
from .models import Cita


class CitaListView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = "citas/cita_list.html"
    context_object_name = "object_list"

    def get_queryset(self):
        # ✅ Solo citas del usuario autenticado
        return Cita.objects.filter(usuario=self.request.user).select_related("cliente", "oferta")


class CitaDetailView(LoginRequiredMixin, DetailView):
    model = Cita
    template_name = "citas/cita_detail.html"
    context_object_name = "cita"

    def get_queryset(self):
        # ✅ Solo citas del usuario autenticado
        return Cita.objects.filter(usuario=self.request.user)


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

        if not cliente_id and nombre:
            cliente = Cliente.objects.create(
                nombre=nombre,
                telefono=telefono if telefono else None,
                usuario=self.request.user
            )
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
        elif cliente_id:
            try:
                cliente = Cliente.objects.get(pk=cliente_id)
            except Cliente.DoesNotExist:
                form.add_error("cliente", "El cliente seleccionado no existe")
                return self.form_invalid(form)

        if not cliente:
            form.add_error("cliente", "Debes seleccionar o crear un cliente")
            return self.form_invalid(form)

        form.instance.cliente = cliente
        form.instance.usuario = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["GOOGLE_MAPS_API_KEY"] = settings.GOOGLE_MAPS_API_KEY
        return context


class CitaCreateView(LoginRequiredMixin, CreateView):
    model = Cita
    fields = ['cliente', 'fecha', 'recordatorio', 'oferta', 'estado']
    template_name = "citas/cita_form.html"
    success_url = reverse_lazy('cita_list')
    extra_context = {"titulo": "Nueva Cita"}

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class CitaUpdateView(LoginRequiredMixin, UpdateView):
    model = Cita
    fields = ['cliente', 'fecha', 'recordatorio', 'oferta', 'estado']
    template_name = "citas/cita_form.html"
    success_url = reverse_lazy('cita_list')
    extra_context = {"titulo": "Editar Cita"}


class CitaDeleteView(LoginRequiredMixin, DeleteView):
    model = Cita
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy('cita_list')
    extra_context = {"titulo": "Eliminar Cita"}
