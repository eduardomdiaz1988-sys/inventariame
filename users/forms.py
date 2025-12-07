from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

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
