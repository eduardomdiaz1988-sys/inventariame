from django.urls import path
from .views import DireccionListView, DireccionCreateView,map_view, save_address

urlpatterns = [
    path('direcciones/', DireccionListView.as_view(), name='direccion_list'),
    path('direcciones/nueva/', DireccionCreateView.as_view(), name='direccion_create'),
    path("mapa/", map_view, name="location_map"),
    path("api/direcciones/", save_address, name="location_save_address"),
]
