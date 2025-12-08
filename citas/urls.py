from django.urls import path
from .views import (

    CitaListView, CitaCreateView, CitaUpdateView, CitaDeleteView,CitaCreateWithClientView
)

urlpatterns = [
    path('', CitaListView.as_view(), name='cita_list'),
    path('nueva/', CitaCreateView.as_view(), name='cita_create'),
    path('nueva_cita/', CitaCreateWithClientView.as_view(), name='cita_create_card'),
    path('<int:pk>/editar/', CitaUpdateView.as_view(), name='cita_update'),
    path('<int:pk>/eliminar/', CitaDeleteView.as_view(), name='cita_delete'),
]
