# mantenimientos/views.py
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Sum
from .models import Mantenimiento, ConfiguracionMantenimientos
from .forms import MantenimientoForm, ConfiguracionForm
import datetime, calendar, json
class MantenimientoListView(LoginRequiredMixin, ListView):
    model = Mantenimiento
    template_name = "mantenimientos/mantenimiento_list.html"
    context_object_name = "mantenimientos"

    def get_queryset(self):
        return Mantenimiento.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        hoy = datetime.date.today()
        ayer = hoy - datetime.timedelta(days=1)

        # Configuración de festivos persistente por usuario/mes
        config = ConfiguracionMantenimientos.objects.filter(
            usuario=self.request.user, año=hoy.year, mes=hoy.month
        ).first()
        dias_festivos = config.dias_festivos if config else 0

        # Días del mes y laborables
        _, num_days = calendar.monthrange(hoy.year, hoy.month)
        dias_mes = [datetime.date(hoy.year, hoy.month, d) for d in range(1, num_days+1)]
        dias_laborables = [d for d in dias_mes if d.weekday() < 5]  # 0-4: L-V

        # Meta ajustada por festivos
        dias_laborables_ajustados = max(len(dias_laborables) - dias_festivos, 0)
        meta_mensual = dias_laborables_ajustados * 7

        # Producción del mes (todas las fechas)
        produccion_mes = qs.filter(fecha__month=hoy.month).aggregate(Sum("cantidad"))["cantidad__sum"] or 0

        # Producción L-V
        produccion_lv = qs.filter(fecha__month=hoy.month, fecha__week_day__in=[2,3,4,5,6]) \
                          .aggregate(Sum("cantidad"))["cantidad__sum"] or 0
        dias_lv_registrados = qs.filter(fecha__month=hoy.month, fecha__week_day__in=[2,3,4,5,6]).count()
        media_lv = produccion_lv / dias_lv_registrados if dias_lv_registrados else 0

        # Producción sábados
        produccion_sabados = qs.filter(fecha__month=hoy.month, fecha__week_day=7) \
                               .aggregate(Sum("cantidad"))["cantidad__sum"] or 0

        # Lógica de inclusión de sábados según media L-V
        if media_lv < 7:
            produccion_total = produccion_mes   # sábados sí cuentan
            extras = 0
        else:
            produccion_total = produccion_lv    # sábados cuentan como extra
            extras = produccion_sabados

        cumplimiento = round((produccion_total / meta_mensual) * 100, 2) if meta_mensual else 0

        # Datos para gráfico (últimos 30 días)
        ultimos = qs.filter(fecha__gte=hoy - datetime.timedelta(days=30)).order_by("fecha")
        dias = [m.fecha.strftime("%Y-%m-%d") for m in ultimos]
        cantidades = [m.cantidad for m in ultimos]

        # --- Mensaje motivador dinámico ---
        hoy_count = qs.filter(fecha=hoy).aggregate(Sum("cantidad"))["cantidad__sum"] or 0
        ayer_count = qs.filter(fecha=ayer).aggregate(Sum("cantidad"))["cantidad__sum"] or 0

        if hoy_count > 0:
            if hoy_count > ayer_count:
                mensaje = f"{self.request.user.first_name or self.request.user.username}, eres el mejor 💪. Hoy hiciste {hoy_count} mantenimientos, ¡superaste tu marca de ayer ({ayer_count})!"
            elif hoy_count == ayer_count:
                mensaje = f"{self.request.user.first_name or self.request.user.username}, ¡constancia total! Hoy hiciste {hoy_count} mantenimientos, igual que ayer."
            else:
                mensaje = f"{self.request.user.first_name or self.request.user.username}, hiciste {hoy_count} mantenimientos hoy, un poco menos que ayer ({ayer_count}). ¡Ánimo, mañana más!"
        else:
            mensaje = f"{self.request.user.first_name or self.request.user.username}, aún no registraste mantenimientos hoy. ¡Dale caña!"

        # Actualizar contexto
        context.update({
            "today": hoy,
            "dias_festivos": dias_festivos,
            "meta_mensual": meta_mensual,
            "produccion_total": produccion_total,
            "cumplimiento": cumplimiento,
            "media_lv": round(media_lv, 2),
            "extras": extras,
            "dias_json": json.dumps(dias),
            "cantidades_json": json.dumps(cantidades),
            "mensaje_motivador": mensaje,
        })
        return context


class MantenimientoDetailView(LoginRequiredMixin, DetailView):
    model = Mantenimiento
    template_name = "mantenimientos/mantenimiento_detail.html"
    context_object_name = "mantenimiento"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = datetime.date.today()
        inicio_semana = hoy - datetime.timedelta(days=7)

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

class ConfiguracionUpdateView(LoginRequiredMixin, UpdateView):
    model = ConfiguracionMantenimientos
    form_class = ConfiguracionForm
    template_name = "mantenimientos/configuracion_form.html"
    success_url = reverse_lazy("mantenimiento_list")

    def get_object(self, queryset=None):
        hoy = datetime.date.today()
        obj, _ = ConfiguracionMantenimientos.objects.get_or_create(
            usuario=self.request.user, año=hoy.year, mes=hoy.month
        )
        return obj
