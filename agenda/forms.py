# calendario/forms.py
from django import forms
import datetime
from .models import Festivo

class FestivoForm(forms.ModelForm):
    class Meta:
        model = Festivo
        fields = ["fecha", "descripcion"]
        widgets = {
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control", "placeholder": "Opcional"}),
        }

class FestivosMesForm(forms.Form):
    año = forms.IntegerField(min_value=2000, max_value=2100, label="Año")
    mes = forms.IntegerField(min_value=1, max_value=12, label="Mes")
    fechas = forms.CharField(label="Seleccionar festivos", widget=forms.TextInput(attrs={
        "placeholder": "Selecciona fechas en el calendario",
        "data-flatpickr": "true",
    }))

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
