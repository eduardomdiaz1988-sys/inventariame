from django import forms
from .models import Referencia, Tipo

class TipoForm(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"})
        }

class ReferenciaForm(forms.ModelForm):
    class Meta:
        model = Referencia
        fields = ["nombre", "tipo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-control"})
        }
