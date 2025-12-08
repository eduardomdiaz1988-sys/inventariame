from django.urls import path
from . import views

urlpatterns = [
    # Tipos
    path("tipos/", views.tipo_list, name="tipo_list"),
    path("tipos/nuevo/", views.tipo_nuevo, name="tipo_nuevo"),
    path("tipos/<int:pk>/editar/", views.tipo_editar, name="tipo_editar"),
    path("tipos/<int:pk>/eliminar/", views.tipo_eliminar, name="tipo_eliminar"),

    # Referencias
    path("referencias/", views.referencia_list, name="referencia_list"),
    path("referencias/nuevo/", views.referencia_nuevo, name="referencia_nuevo"),
    path("referencias/<int:pk>/editar/", views.referencia_editar, name="referencia_editar"),
    path("referencias/<int:pk>/eliminar/", views.referencia_eliminar, name="referencia_eliminar"),
]
