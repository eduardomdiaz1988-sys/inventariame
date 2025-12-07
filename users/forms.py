from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from users.models import PerfilUsuario

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    matricula = forms.CharField(max_length=50, required=False)
    nombre_grupo = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2", "matricula", "nombre_grupo"]

    def save(self, commit=True, tipo_usuario="individual"):
        user = super().save(commit=commit)

        # Crear o asignar grupo de Django
        grupo_obj, _ = Group.objects.get_or_create(name=tipo_usuario.capitalize())
        user.groups.add(grupo_obj)

        # Crear perfil asociado
        PerfilUsuario.objects.create(
            usuario=user,
            tipo_usuario=tipo_usuario,
            matricula=self.cleaned_data.get("matricula"),
            nombre_grupo=self.cleaned_data.get("nombre_grupo"),
            grupo_django=grupo_obj
        )

        return user
