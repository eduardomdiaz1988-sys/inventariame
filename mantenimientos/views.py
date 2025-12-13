from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Sum, Avg, Max
from .models import Mantenimiento
from .forms import MantenimientoForm
import datetime
import json

class MantenimientoListView(LoginRequiredMixin, ListView):
    model = Mantenimiento
    template_name = "mantenimientos/mantenimiento_list.html"
    context_object_name = "mantenimientos"

    def get_queryset(self):
        qs = Mantenimiento.objects.filter(usuario=self.request.user)
        start = self.request.GET.get("start")
        end = self.request.GET.get("end")
        if start and end:
            qs = qs.filter(fecha__range=[start, end])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()

        # Estadísticas rápidas
        hoy = datetime.date.today()
        context["today"] = hoy
        context["total_mes"] = qs.filter(fecha__month=hoy.month).aggregate(Sum("cantidad"))["cantidad__sum"] or 0
        context["promedio"] = round(qs.aggregate(Avg("cantidad"))["cantidad__avg"] or 0, 2)
        context["maximo"] = qs.aggregate(Max("cantidad"))["cantidad__max"] or 0

        # Datos para gráfico (últimos 30 días)
        ultimos = qs.filter(fecha__gte=hoy - datetime.timedelta(days=30)).order_by("fecha")
        dias = [m.fecha.strftime("%Y-%m-%d") for m in ultimos]
        cantidades = [m.cantidad for m in ultimos]
        context["dias_json"] = json.dumps(dias)
        context["cantidades_json"] = json.dumps(cantidades)

        return context

class MantenimientoDetailView(LoginRequiredMixin, DetailView):
    model = Mantenimiento
    template_name = "mantenimientos/mantenimiento_detail.html"
    context_object_name = "mantenimiento"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = datetime.date.today()
        inicio_semana = hoy - datetime.timedelta(days=7)

        # Últimos 7 días del mismo usuario
        qs = Mantenimiento.objects.filter(
            usuario=self.request.user,
            fecha__gte=inicio_semana,
            fecha__lte=hoy
        ).order_by("fecha")

        dias = [m.fecha.strftime("%Y-%m-%d") for m in qs]
        cantidades = [m.cantidad for m in qs]

        context["dias_json"] = json.dumps(dias)
        context["cantidades_json"] = json.dumps(cantidades)
        return context

class MantenimientoCreateView(LoginRequiredMixin, CreateView):
    model = Mantenimiento
    form_class = MantenimientoForm
    template_name = "mantenimientos/mantenimiento_form.html"
    success_url = reverse_lazy("mantenimiento_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
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
