from django import forms
from core.models import Cita

class CitaForm(forms.ModelForm):
    fecha = forms.DateTimeField(
        widget=forms.TextInput(attrs={
            "id": "fecha",
            "class": "form-control",
            "placeholder": "Selecciona fecha y hora"
        }),
        input_formats=["%Y-%m-%d %H:%M"]
    )

    class Meta:
        model = Cita
        fields = ["cliente", "direccion", "fecha", "recordatorio", "oferta"]  # añadimos oferta
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-control"}),
            "direccion": forms.Select(attrs={"class": "form-control"}),
            "recordatorio": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "oferta": forms.Select(attrs={"class": "form-control"}),  # nuevo campo
        }
