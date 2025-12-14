# agenda/urls.py
from django.urls import path
from .views import AgendaCalendarView, CitasEventsApi, VentasEventsApi,EventosApi,festivos_mes_view, festivo_delete_view

app_name = "agenda"
# calendario/urls.py

urlpatterns = [
    path("", AgendaCalendarView.as_view(), name="calendar"),
    path("api/citas/", CitasEventsApi.as_view(), name="api_citas"),
    path("api/ventas/", VentasEventsApi.as_view(), name="api_ventas"),
    path("api/eventos/", EventosApi.as_view(), name="api_eventos"),
]

urlpatterns += [
    path("festivos/", festivos_mes_view, name="festivos_mes"),
    path("festivos/<int:pk>/delete/", festivo_delete_view, name="festivo_delete"),
]
