# mantenimientos/forms.py
from django import forms
from .models import Mantenimiento, ConfiguracionMantenimientos
import datetime

class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        fields = ["fecha", "cantidad"]
        widgets = {
            "fecha": forms.DateInput(attrs={
                "class": "form-control flatpickr",
                "placeholder": "Selecciona fecha"
            }),
            "cantidad": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
                "max": 15
            }),
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
    """
    Formulario clásico para editar directamente el número de días festivos.
    Se mantiene por compatibilidad, aunque ahora se recomienda usar FestivosConfigForm
    para seleccionar fechas y sincronizar automáticamente.
    """
    class Meta:
        model = ConfiguracionMantenimientos
        fields = ["año", "mes", "dias_festivos"]
        widgets = {
            "año": forms.NumberInput(attrs={"class": "form-control"}),
            "mes": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 12}),
            "dias_festivos": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 31}),
        }


class FestivosConfigForm(forms.Form):
    """
    Formulario para seleccionar múltiples fechas festivas con Flatpickr.
    Al guardar, se crean las fechas en agenda.Festivo y se actualiza
    ConfiguracionMantenimientos.dias_festivos con el total de festivos laborables.
    """
    año = forms.IntegerField(min_value=2000, max_value=2100, label="Año")
    mes = forms.IntegerField(min_value=1, max_value=12, label="Mes")
    fechas = forms.CharField(
        label="Seleccionar festivos",
        widget=forms.TextInput(attrs={
            "placeholder": "Selecciona fechas en el calendario",
            "data-flatpickr": "true",
        }),
        required=False
    )

    def clean(self):
        cleaned = super().clean()
        año = cleaned.get("año")
        mes = cleaned.get("mes")
        fechas_str = cleaned.get("fechas", "").strip()

        if not fechas_str:
            cleaned["fechas_lista"] = []
            return cleaned

        try:
            partes = [f.strip() for f in fechas_str.split(",") if f.strip()]
            fechas = [datetime.date.fromisoformat(p) for p in partes]
        except ValueError:
            raise forms.ValidationError("Formato de fechas inválido. Usa YYYY-MM-DD.")

        for f in fechas:
            if f.year != año or f.month != mes:
                raise forms.ValidationError(f"La fecha {f} no pertenece a {mes}/{año}.")

        cleaned["fechas_lista"] = fechas
        return cleaned
