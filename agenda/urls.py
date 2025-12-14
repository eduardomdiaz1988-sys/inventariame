from django.urls import path
from .views import (
    AgendaCalendarView,
    CitasEventsApi,
    VentasEventsApi,
    EventosApi,
    festivos_mes_view,
    festivo_delete_view,
    FestivoListView,
    FestivoCreateView,
    FestivoUpdateView,
    FestivoDeleteView,
)

app_name = "agenda"

urlpatterns = [
    # Agenda / APIs
    path("", AgendaCalendarView.as_view(), name="calendar"),
    path("api/citas/", CitasEventsApi.as_view(), name="api_citas"),
    path("api/ventas/", VentasEventsApi.as_view(), name="api_ventas"),
    path("api/eventos/", EventosApi.as_view(), name="api_eventos"),

    # Festivos CRUD clásico
    path("festivos/lista/", FestivoListView.as_view(), name="festivo_list"),
    path("festivos/nuevo/", FestivoCreateView.as_view(), name="festivo_create"),
    path("festivos/<int:pk>/editar/", FestivoUpdateView.as_view(), name="festivo_update"),
    path("festivos/<int:pk>/eliminar/", FestivoDeleteView.as_view(), name="festivo_delete"),

    # Festivos gestión por mes
    path("festivos/mes/", festivos_mes_view, name="festivos_mes"),

    # Festivos eliminación AJAX
    path("festivos/<int:pk>/delete-ajax/", festivo_delete_view, name="festivo_delete_ajax"),
]
