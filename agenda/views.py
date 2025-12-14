# agenda/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
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

@login_required
def festivos_mes_view(request):
    if request.method == "POST":
        form = FestivosMesForm(request.POST)
        if form.is_valid():
            año = form.cleaned_data["año"]
            mes = form.cleaned_data["mes"]
            fechas = form.cleaned_data["fechas_lista"]

            creadas = 0
            for f in fechas:
                try:
                    _, created = Festivo.objects.get_or_create(fecha=f)
                    if created:
                        creadas += 1
                except IntegrityError:
                    continue

            total_mes = Festivo.objects.filter(fecha__year=año, fecha__month=mes).count()
            messages.success(request, f"Festivos guardados. Nuevos: {creadas}. Total en {mes}/{año}: {total_mes}.")
            return redirect("festivos_mes")
    else:
        import datetime
        hoy = datetime.date.today()
        form = FestivosMesForm(initial={"año": hoy.year, "mes": hoy.month})

    año = form.initial.get("año") if not form.is_bound else form.data.get("año", form.initial.get("año"))
    mes = form.initial.get("mes") if not form.is_bound else form.data.get("mes", form.initial.get("mes"))

    existentes = []
    try:
        año_int = int(año)
        mes_int = int(mes)
        existentes = Festivo.objects.filter(fecha__year=año_int, fecha__month=mes_int).order_by("fecha")
    except Exception:
        pass

    return render(request, "agenda/festivos_form.html", {
        "form": form,
        "existentes": existentes,
    })

@require_POST
@login_required
def festivo_delete_view(request, pk):
    festivo = get_object_or_404(Festivo, pk=pk)
    festivo.delete()
    messages.info(request, f"Festivo {festivo.fecha} eliminado.")
    return redirect("festivos_mes")

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
