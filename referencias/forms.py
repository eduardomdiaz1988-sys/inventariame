# referencias/forms.py
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
        fields = ["nombre", "tipo", "valor"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "valor": forms.Select(
                choices=[(3, "0 + 3"), (4, "0 + 4"), (5, "0 + 5"), (7, "0 + 7"), (10, "0 + 10")],
                attrs={"class": "form-control"}
            ),
        }
