from django import forms
from .models import Oferta

class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ["nombre", "referencia", "tipo", "valor"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "referencia": forms.Select(attrs={"class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "valor": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: 0 + 7"}),
        }
