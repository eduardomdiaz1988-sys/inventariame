from django.urls import path
from .views import (
    ElementoListView, ElementoCreateView, ElementoUpdateView, ElementoDeleteView,
    StockListView, StockCreateView, StockUpdateView, StockDeleteView,
    CantidadListView, CantidadCreateView, CantidadUpdateView, CantidadDeleteView,
    CantidadAdjustView,api_buscar_elemento
)

urlpatterns = [
    path('elementos/', ElementoListView.as_view(), name='elemento_list'),
    path('elementos/nuevo/', ElementoCreateView.as_view(), name='elemento_create'),
    path('elementos/<int:pk>/editar/', ElementoUpdateView.as_view(), name='elemento_update'),
    path('elementos/<int:pk>/eliminar/', ElementoDeleteView.as_view(), name='elemento_delete'),

    path('stocks/', StockListView.as_view(), name='stock_list'),
    path('stocks/nuevo/', StockCreateView.as_view(), name='stock_create'),
    path('stocks/<int:pk>/editar/', StockUpdateView.as_view(), name='stock_update'),
    path('stocks/<int:pk>/eliminar/', StockDeleteView.as_view(), name='stock_delete'),

    path('cantidades/', CantidadListView.as_view(), name='cantidad_list'),
    path('cantidades/nueva/', CantidadCreateView.as_view(), name='cantidad_create'),
    path('cantidades/<int:pk>/editar/', CantidadUpdateView.as_view(), name='cantidad_update'),
    path('cantidades/<int:pk>/eliminar/', CantidadDeleteView.as_view(), name='cantidad_delete'),
    path('cantidades/ajustar/', CantidadAdjustView.as_view(), name='cantidad_adjust'),


    path("api/elementos/", api_buscar_elemento, name="api_buscar_elemento"),

]
