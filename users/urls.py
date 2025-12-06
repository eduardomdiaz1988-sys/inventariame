from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home_view, registro_view, buscar_view,logout_view,verificar_usuario

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
    path("logout/", logout_view, name="logout"), 
    path('registro/', registro_view, name='registro'),
    path('buscar/', buscar_view, name='buscar'),
    path("verificar-usuario/", verificar_usuario, name="verificar_usuario"),

]
