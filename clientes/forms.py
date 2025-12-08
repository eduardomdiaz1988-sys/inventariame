from django import forms
from .models import Cliente
from locations.models import Address

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
