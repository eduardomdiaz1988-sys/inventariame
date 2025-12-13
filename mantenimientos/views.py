from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Mantenimiento
from .forms import MantenimientoForm

class MantenimientoListView(LoginRequiredMixin, ListView):
    model = Mantenimiento
    template_name = "mantenimientos/mantenimiento_list.html"
    context_object_name = "mantenimientos"

    def get_queryset(self):
        # Opcional: mostrar solo mantenimientos del usuario
        return Mantenimiento.objects.filter(usuario=self.request.user)

class MantenimientoDetailView(LoginRequiredMixin, DetailView):
    model = Mantenimiento
    template_name = "mantenimientos/mantenimiento_detail.html"
    context_object_name = "mantenimiento"

class MantenimientoCreateView(LoginRequiredMixin, CreateView):
    model = Mantenimiento
    form_class = MantenimientoForm
    template_name = "mantenimientos/mantenimiento_form.html"
    success_url = reverse_lazy("mantenimiento_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pasar el usuario al formulario para asignarlo al instance antes de validar
        kwargs["user"] = self.request.user
        return kwargs

class MantenimientoUpdateView(LoginRequiredMixin, UpdateView):
    model = Mantenimiento
    form_class = MantenimientoForm
    template_name = "mantenimientos/mantenimiento_form.html"
    success_url = reverse_lazy("mantenimiento_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

class MantenimientoDeleteView(LoginRequiredMixin, DeleteView):
    model = Mantenimiento
    template_name = "mantenimientos/mantenimiento_confirm_delete.html"
    success_url = reverse_lazy("mantenimiento_list")
