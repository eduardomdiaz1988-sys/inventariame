# mantenimientos/urls.py
from django.urls import path
from .views import (
    MantenimientoListView, MantenimientoDetailView,
    MantenimientoCreateView, MantenimientoUpdateView, MantenimientoDeleteView,
    configurar_festivos_view
)

urlpatterns = [
    path("", MantenimientoListView.as_view(), name="mantenimiento_list"),
    path("detalle/<int:pk>/", MantenimientoDetailView.as_view(), name="mantenimiento_detail"),
    path("crear/", MantenimientoCreateView.as_view(), name="mantenimiento_create"),
    path("editar/<int:pk>/", MantenimientoUpdateView.as_view(), name="mantenimiento_update"),
    path("eliminar/<int:pk>/", MantenimientoDeleteView.as_view(), name="mantenimiento_delete"),

    path("festivos/", configurar_festivos_view, name="configurar_festivos"),
]
