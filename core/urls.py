from django.urls import path
from .views import (

    CitaListView, CitaCreateView, CitaUpdateView, CitaDeleteView
)

urlpatterns = [
  
    path('citas/', CitaListView.as_view(), name='cita_list'),
    path('citas/nueva/', CitaCreateView.as_view(), name='cita_create'),
    path('citas/<int:pk>/editar/', CitaUpdateView.as_view(), name='cita_update'),
    path('citas/<int:pk>/eliminar/', CitaDeleteView.as_view(), name='cita_delete'),
]
