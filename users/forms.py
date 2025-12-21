from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from .models import  PerfilUsuario

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
        
class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ["matricula", "nombre_grupo", "tipo_usuario"]
        widgets = {
            "matricula": forms.TextInput(attrs={"class": "form-control"}),
            "nombre_grupo": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_usuario": forms.Select(attrs={"class": "form-select"}),
        }

class RegistroBasicoForm(UserCreationForm):
    matricula = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "matricula"]

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    matricula = forms.CharField(max_length=50, required=False)
    nombre_grupo = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "matricula",
            "nombre_grupo",
        ]

    def save(self, commit=True, tipo_usuario="individual"):
        user = super().save(commit=commit)

        # Crear o asignar grupo de Django
        grupo_obj, _ = Group.objects.get_or_create(name=tipo_usuario.capitalize())
        user.groups.add(grupo_obj)

        # ⚠️ Importante: NO crear PerfilUsuario aquí
        # La señal en models.py se encargará de hacerlo automáticamente

        return user
