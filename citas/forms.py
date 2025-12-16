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
        # Usa SOLO fields (no mezcles con exclude)
        fields = ["fecha", "oferta", "numero_instalacion"]
        widgets = {
            # cliente viene del input hidden de tu plantilla (paso 2), lo mantenemos oculto aquí también
            "cliente": forms.HiddenInput(),
            "oferta": forms.Select(attrs={"class": "form-control", "id": "id_oferta"}),
            "numero_instalacion": forms.NumberInput(attrs={"class": "form-control", "id": "id_numero_instalacion"}),
        }


class CitaForm(forms.ModelForm):
    # Si mantienes la vista simple, usa el mismo id para armonizar con flatpickr
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
        # Usa SOLO fields. No incluimos recordatorio ni estado.
        fields = ["cliente", "fecha", "oferta", "numero_instalacion"]
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-control", "id": "id_cliente"}),
            "oferta": forms.Select(attrs={"class": "form-control", "id": "id_oferta"}),
            "numero_instalacion": forms.NumberInput(attrs={"class": "form-control", "id": "id_numero_instalacion"}),
        }
