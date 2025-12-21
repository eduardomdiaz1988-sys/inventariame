from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home_view, perfil_editar, registro_basic_view, registro_view, buscar_view, logout_view, verificar_usuario, perfil_view

app_name = "users"

urlpatterns = [
    path('dashboard', home_view, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
    path("logout/", logout_view, name="logout"), 
    path('registro/', registro_view, name='registro'),
    path('buscar/', buscar_view, name='buscar'),
    path("verificar-usuario/", verificar_usuario, name="verificar_usuario"),
    path("perfil/", perfil_view, name="perfil"),  
    path("perfil/editar/", perfil_editar, name="perfil_editar"),
    path("registro-basico/", registro_basic_view, name="registro_basico"),
]
