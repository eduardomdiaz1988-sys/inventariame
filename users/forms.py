from django import forms
from django.contrib.auth.models import User, Group
from .models import PerfilUsuario

class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)
    matricula = forms.CharField(label="Matrícula")
    grupo = forms.ModelChoiceField(queryset=Group.objects.all(), label="Grupo")

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            PerfilUsuario.objects.create(
                user=user,
                matricula=self.cleaned_data["matricula"],
                grupo_django=self.cleaned_data["grupo"]
            )
        return user
