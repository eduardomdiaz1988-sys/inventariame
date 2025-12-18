# citas/forms.py
from django import forms
from citas.models import Cita

class CitaWithClientForm(forms.ModelForm):
    fecha = forms.DateTimeField(
        widget=forms.TextInput(attrs={
            "id": "id_fecha",  # importante para flatpickr
            "class": "form-control",
            "placeholder": "Selecciona fecha y hora"
        }),
        input_formats=["%Y-%m-%d %H:%M"]
    )

    class Meta:
        model = Cita
        # ✅ añadimos observaciones
        fields = ["fecha", "oferta", "numero_instalacion", "observaciones"]
        widgets = {
            "cliente": forms.HiddenInput(),
            "oferta": forms.Select(attrs={"class": "form-control", "id": "id_oferta"}),
            "numero_instalacion": forms.NumberInput(attrs={"class": "form-control", "id": "id_numero_instalacion"}),
            "observaciones": forms.Textarea(attrs={
                "class": "form-control",
                "id": "id_observaciones",
                "rows": 4,
                "placeholder": "Añade observaciones o notas adicionales..."
            }),
        }


class CitaForm(forms.ModelForm):
    fecha = forms.DateTimeField(
        widget=forms.TextInput(attrs={
            "id": "id_fecha",
            "class": "form-control",
            "placeholder": "Selecciona fecha y hora"
        }),
        input_formats=["%Y-%m-%d %H:%M"]
    )

    class Meta:
        model = Cita
        # ✅ añadimos observaciones también aquí
        fields = ["cliente", "fecha", "oferta", "numero_instalacion", "observaciones"]
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-control", "id": "id_cliente"}),
            "oferta": forms.Select(attrs={"class": "form-control", "id": "id_oferta"}),
            "numero_instalacion": forms.NumberInput(attrs={"class": "form-control", "id": "id_numero_instalacion"}),
            "observaciones": forms.Textarea(attrs={
                "class": "form-control",
                "id": "id_observaciones",
                "rows": 4,
                "placeholder": "Añade observaciones o notas adicionales..."
            }),
        }
