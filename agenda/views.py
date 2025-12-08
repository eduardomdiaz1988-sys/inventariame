# agenda/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.utils.timezone import make_aware
from datetime import datetime
from citas.models import Cita
from sales.models import Venta  # ajusta si tu app se llama distinto
from django.views.generic import View



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
