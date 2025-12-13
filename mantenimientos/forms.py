# mantenimientos/forms.py
from django import forms
from .models import Mantenimiento, ConfiguracionMantenimientos
import datetime

class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        fields = ["fecha", "cantidad"]
        widgets = {
            "fecha": forms.DateInput(attrs={"class": "form-control flatpickr", "placeholder": "Selecciona fecha"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 15}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user and not self.instance.usuario_id:
            self.instance.usuario = self.user
        if not self.instance.pk and not self.initial.get("fecha"):
            self.initial["fecha"] = datetime.date.today()

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get("cantidad")
        if cantidad is None:
            return cantidad
        if cantidad < 0:
            raise forms.ValidationError("La cantidad no puede ser menor que 0.")
        if cantidad > 15:
            raise forms.ValidationError("La cantidad no puede ser mayor que 15.")
        return cantidad

class ConfiguracionForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionMantenimientos
        fields = ["año", "mes", "dias_festivos"]
        widgets = {
            "año": forms.NumberInput(attrs={"class": "form-control"}),
            "mes": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 12}),
            "dias_festivos": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 31}),
        }
