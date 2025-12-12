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
        exclude = ["cliente", "usuario"]
        fields = ["cliente", "fecha", "recordatorio", "oferta", "estado"]
        widgets = {
            "cliente": forms.HiddenInput(),  # lo rellena el JS en la vista completa
            "recordatorio": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "id_recordatorio"}),
            "oferta": forms.Select(attrs={"class": "form-control", "id": "id_oferta"}),
            "estado": forms.Select(attrs={"class": "form-control", "id": "id_estado"}),
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
        # 🔥 Quitamos 'direccion' porque NO existe en el modelo
        fields = ["cliente", "fecha", "recordatorio", "oferta", "estado"]
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-control", "id": "id_cliente"}),
            "recordatorio": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "id_recordatorio"}),
            "oferta": forms.Select(attrs={"class": "form-control", "id": "id_oferta"}),
            "estado": forms.Select(attrs={"class": "form-control", "id": "id_estado"}),
        }
