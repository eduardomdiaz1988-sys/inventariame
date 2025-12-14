# forms.py
from django import forms
from .models import Oferta

class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ["nombre", "referencia", "valor"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "referencia": forms.Select(attrs={"class": "form-control"}),
            "valor": forms.Select(
                choices=[(3, "0 + 3"), (4, "0 + 4"), (5, "0 + 5"), (7, "0 + 7"), (10, "0 + 10")],
                attrs={"class": "form-control"}
            ),
        }
