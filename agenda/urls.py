# agenda/urls.py
from django.urls import path
from .views import AgendaCalendarView, CitasEventsApi, VentasEventsApi,EventosApi

app_name = "agenda"

urlpatterns = [
    path("", AgendaCalendarView.as_view(), name="calendar"),
    path("api/citas/", CitasEventsApi.as_view(), name="api_citas"),
    path("api/ventas/", VentasEventsApi.as_view(), name="api_ventas"),
    path("api/eventos/", EventosApi.as_view(), name="api_eventos"),
]
