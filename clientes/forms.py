from django import forms
from .models import Cliente
from locations.models import Address
from django import forms
from citas.models import Cita

class CitaWithClientForm(forms.ModelForm):
    # Campos de cliente/dirección como hidden
    cliente = forms.IntegerField(required=False, widget=forms.HiddenInput())
    nombre = forms.CharField(required=False, widget=forms.HiddenInput())
    telefono = forms.CharField(required=False, widget=forms.HiddenInput())
    address = forms.CharField(required=False, widget=forms.HiddenInput())
    latitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    longitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    label = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Cita
        fields = [
            "fecha",
            "estado",
            "recordatorio",
            "numero_instalacion",
            "observaciones",

            # cliente y dirección como hidden
            "cliente", "nombre", "telefono", "address", "latitude", "longitude", "label"
        ]
        widgets = {
            "fecha": forms.DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local"
            }),
            "estado": forms.Select(attrs={"class": "form-select"}),
            "recordatorio": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "numero_instalacion": forms.NumberInput(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Añade observaciones o notas adicionales..."
            }),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "telefono", "direccion"]  # añadimos telefono
        widgets = {
            "telefono": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Introduce el teléfono"
            }),
            "direccion": forms.Select(attrs={"class": "form-select"})
        }

    def __init__(self, *args, **kwargs):
        cliente = kwargs.pop("cliente", None)
        super().__init__(*args, **kwargs)
        # Si hay cliente, filtra sus direcciones; si no, deja queryset vacío
        if cliente:
            self.fields["direccion"].queryset = Address.objects.filter(cliente=cliente)
        else:
            self.fields["direccion"].queryset = Address.objects.none()
            self.fields["direccion"].widget.attrs["placeholder"] = "Selecciona después de crear una dirección"
