from django.urls import path
from .views import cliente_list, buscar_cliente,cliente_nuevo, cliente_editar,cliente_eliminar,set_principal

urlpatterns = [
    path("", cliente_list, name="cliente_list"),
    path("nuevo/", cliente_nuevo, name="cliente_nuevo"),
    path("<int:pk>/editar/", cliente_editar, name="cliente_update"),
    path("<int:pk>/eliminar/", cliente_eliminar, name="cliente_delete"),
    # Opcional: endpoint para setear principal vía AJAX
    path("<int:pk>/direccion-principal/", set_principal, name="clientes_set_principal"),

    path("api/buscar/", buscar_cliente, name="cliente_buscar"),
]
