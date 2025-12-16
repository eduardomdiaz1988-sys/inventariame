from django.urls import path
from . import views

urlpatterns = [
    path("", views.oferta_list, name="oferta_list"),
    path("nueva/", views.oferta_nueva, name="oferta_nueva"),
    path("<int:pk>/editar/", views.oferta_editar, name="oferta_editar"),
    path("<int:pk>/eliminar/", views.oferta_eliminar, name="oferta_eliminar"),
    path("<int:pk>/detail/", views.oferta_detail, name="oferta_detail"),
    path("api/buscar/", views.buscar_ofertas, name="oferta_buscar_api"),
]
