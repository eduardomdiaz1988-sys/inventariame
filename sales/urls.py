from django.urls import path
from .views import VentaListView, VentaCreateView, VentaUpdateView, VentaDeleteView

urlpatterns = [
    path('ventas/', VentaListView.as_view(), name='venta_list'),
    path('ventas/nueva/', VentaCreateView.as_view(), name='venta_create'),
    path('ventas/<int:pk>/editar/', VentaUpdateView.as_view(), name='venta_update'),
    path('ventas/<int:pk>/eliminar/', VentaDeleteView.as_view(), name='venta_delete'),
]
