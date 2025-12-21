# citas/forms.py
from django import forms
from citas.models import Cita

class CitaWithClientForm(forms.ModelForm):
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
        fields = ["fecha", "numero_instalacion", "observaciones"]  # ❌ oferta eliminada
        widgets = {
            "numero_instalacion": forms.NumberInput(attrs={
                "class": "form-control",
                "id": "id_numero_instalacion"
            }),
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
        fields = [
            "cliente",
            "fecha",
            "estado",           # ✅ Añadido
            "recordatorio",     # ✅ Añadido
            "numero_instalacion",
            "observaciones"
        ]
        widgets = {
            "cliente": forms.Select(attrs={
                "class": "form-control",
                "id": "id_cliente"
            }),
            "estado": forms.Select(attrs={
                "class": "form-select",
                "id": "id_estado"
            }),
            "recordatorio": forms.CheckboxInput(attrs={
                "class": "form-check-input",
                "id": "id_recordatorio"
            }),
            "numero_instalacion": forms.NumberInput(attrs={
                "class": "form-control",
                "id": "id_numero_instalacion"
            }),
            "observaciones": forms.Textarea(attrs={
                "class": "form-control",
                "id": "id_observaciones",
                "rows": 4,
                "placeholder": "Añade observaciones o notas adicionales..."
            }),
        }
