from django.urls import path
from . import views

urlpatterns = [
    path("", views.MantenimientoListView.as_view(), name="mantenimiento_list"),
    path("<int:pk>/", views.MantenimientoDetailView.as_view(), name="mantenimiento_detail"),
    path("crear/", views.MantenimientoCreateView.as_view(), name="mantenimiento_create"),
    path("<int:pk>/editar/", views.MantenimientoUpdateView.as_view(), name="mantenimiento_update"),
    path("<int:pk>/eliminar/", views.MantenimientoDeleteView.as_view(), name="mantenimiento_delete"),
]
