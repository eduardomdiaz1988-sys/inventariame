# agenda/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.utils.timezone import make_aware
from datetime import datetime
from citas.models import Cita
from sales.models import Venta  # ajusta si tu app se llama distinto
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from .forms import FestivosMesForm
from .models import Festivo
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import FestivoForm, FestivosMesForm
class FestivoListView(LoginRequiredMixin, ListView):
    model = Festivo
    template_name = "agenda/festivo_list.html"

    def get_queryset(self):
        # ✅ Solo los festivos del usuario actual
        return Festivo.objects.filter(usuario=self.request.user).order_by("fecha")


class FestivoCreateView(LoginRequiredMixin, CreateView):
    model = Festivo
    form_class = FestivoForm
    template_name = "agenda/festivo_form.html"
    success_url = reverse_lazy("agenda:festivo_list")  # ✅ usa namespace

    def form_valid(self, form):
        # ✅ asignar siempre el usuario
        form.instance.usuario = self.request.user
        try:
            return super().form_valid(form)
        except Exception:
            form.add_error("fecha", "Ya tienes un festivo en esta fecha.")
            return self.form_invalid(form)


class FestivoUpdateView(LoginRequiredMixin, UpdateView):
    model = Festivo
    form_class = FestivoForm
    template_name = "agenda/festivo_form.html"
    success_url = reverse_lazy("agenda:festivo_list")  # ✅ usa namespace

    def get_queryset(self):
        return Festivo.objects.filter(usuario=self.request.user)


class FestivoDeleteView(LoginRequiredMixin, DeleteView):
    model = Festivo
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy("agenda:festivo_list")  # ✅ usa namespace

    def get_queryset(self):
        return Festivo.objects.filter(usuario=self.request.user)


@login_required
def festivos_mes_view(request):
    if request.method == "POST":
        form = FestivosMesForm(request.POST)
        if form.is_valid():
            año = form.cleaned_data["año"]
            mes = form.cleaned_data["mes"]
            fechas = form.cleaned_data["fechas_lista"]

            # ✅ Borrar todos los festivos del usuario en ese mes
            Festivo.objects.filter(
                usuario=request.user,
                fecha__year=año,
                fecha__month=mes
            ).delete()

            # ✅ Crear los nuevos seleccionados
            creadas = 0
            for f in fechas:
                festivo, created = Festivo.objects.get_or_create(
                    usuario=request.user, fecha=f
                )
                if created:
                    creadas += 1

            total_mes = Festivo.objects.filter(
                usuario=request.user,
                fecha__year=año,
                fecha__month=mes
            ).count()
            messages.success(
                request,
                f"Festivos actualizados. Nuevos: {creadas}. Total en {mes}/{año}: {total_mes}."
            )
            return redirect("agenda:festivos_mes")  # ✅ usa namespace
    else:
        import datetime
        hoy = datetime.date.today()
        form = FestivosMesForm(initial={"año": hoy.year, "mes": hoy.month})

    año = form.initial.get("año") if not form.is_bound else form.data.get("año", form.initial.get("año"))
    mes = form.initial.get("mes") if not form.is_bound else form.data.get("mes", form.initial.get("mes"))

    existentes_qs = []
    existentes_json = []
    try:
        año_int = int(año)
        mes_int = int(mes)
        existentes_qs = Festivo.objects.filter(
            usuario=request.user,
            fecha__year=año_int,
            fecha__month=mes_int
        ).order_by("fecha")
        existentes_json = list(existentes_qs.values("fecha"))
    except Exception:
        pass

    return render(request, "agenda/festivos_form.html", {
        "form": form,
        "existentes": existentes_qs,        # para listado con botones
        "existentes_json": existentes_json  # para calendario
    })


@require_POST
@login_required
def festivo_delete_view(request, pk):
    festivo = get_object_or_404(Festivo, pk=pk, usuario=request.user)
    fecha = festivo.fecha.isoformat()
    festivo.delete()
    return JsonResponse({"status": "ok", "deleted": pk, "fecha": fecha})

class EventosApi(View):
    def get(self, request):
        events = []

        # Citas
        for c in Cita.objects.filter(usuario=request.user).select_related("cliente"):
            events.append({
                "id": f"cita-{c.id}",
                "title": f"Cita: {getattr(c.cliente, 'nombre', c.cliente_id)}",
                "start": c.fecha.isoformat(),
                "color": "#dc3545",
                "url": f"/citas/{c.pk}/editar/",
                "extendedProps": {
                    "tipo": "cita",
                    "estado": getattr(c, "estado", ""),
                }
            })

        # Ventas
        for v in Venta.objects.filter(usuario=request.user):
            events.append({
                "id": f"venta-{v.id}",
                "title": f"Venta: {getattr(v, 'descripcion', 'Venta')}",
                "start": v.fecha.isoformat(),
                "color": "#0d6efd",
                "url": f"/ventas/{v.pk}/detalle/",
                "extendedProps": {
                    "tipo": "venta",
                    "importe": getattr(v, "importe", None),
                }
            })

        return JsonResponse(events, safe=False)

class AgendaCalendarView(LoginRequiredMixin, TemplateView):
    template_name = "agenda/calendar.html"
    extra_context = {"titulo": "Agenda"}

class CitasEventsApi(LoginRequiredMixin, View):
    def get(self, request):
        start = request.GET.get("start")
        end = request.GET.get("end")
        # FullCalendar envía ISO-8601; convierte si necesitas timezone awareness
        start_dt = make_aware(datetime.fromisoformat(start)) if start else None
        end_dt = make_aware(datetime.fromisoformat(end)) if end else None

        qs = Cita.objects.filter(usuario=request.user)
        if start_dt and end_dt:
            qs = qs.filter(fecha__gte=start_dt, fecha__lte=end_dt)

        events = []
        for c in qs.select_related("cliente"):
            events.append({
                "id": f"cita-{c.id}",
                "title": f"Cita: {getattr(c.cliente, 'nombre', c.cliente_id)}",
                "start": c.fecha.isoformat(),
                # Opción: color según estado
                "color": estado_color(c.estado) if hasattr(c, "estado") else "#dc3545",
                "url": f"/citas/{c.pk}/editar/",  # ajusta a tu ruta real
                "extendedProps": {
                    "tipo": "cita",
                    "cliente": getattr(c.cliente, 'nombre', c.cliente_id),
                    "estado": getattr(c, 'estado', ''),
                }
            })
        return JsonResponse(events, safe=False)

class VentasEventsApi(LoginRequiredMixin, View):
    def get(self, request):
        start = request.GET.get("start")
        end = request.GET.get("end")
        start_dt = datetime.fromisoformat(start).date() if start else None
        end_dt = datetime.fromisoformat(end).date() if end else None

        qs = Venta.objects.filter(usuario=request.user)
        if start_dt and end_dt:
            qs = qs.filter(fecha__gte=start_dt, fecha__lte=end_dt)

        events = []
        for v in qs:
            events.append({
                "id": f"venta-{v.id}",
                "title": f"Venta: {getattr(v, 'descripcion', 'Venta')}",
                "start": v.fecha.isoformat(),  # si es DateField, FullCalendar lo admite
                "color": "#0d6efd",
                "url": f"/ventas/{v.pk}/detalle/",  # ajusta rutas
                "extendedProps": {
                    "tipo": "venta",
                    "importe": getattr(v, 'importe', None),
                }
            })
        return JsonResponse(events, safe=False)

def estado_color(estado):
    # Ajusta a tus estados
    mapa = {
        "pendiente": "#ffc107",
        "confirmada": "#198754",
        "cancelada": "#6c757d",
        "realizada": "#0d6efd",
    }
    return mapa.get(estado, "#dc3545")
