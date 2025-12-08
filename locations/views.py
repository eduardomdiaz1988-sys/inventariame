from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
import json
from .models import Address
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Address



def direcciones_por_cliente(request, cliente_id):
    direcciones = Address.objects.filter(cliente_id=cliente_id).values("id", "address", "label")
    # devolvemos id + texto de la dirección (y opcionalmente el label)
    return JsonResponse(list(direcciones), safe=False)

@login_required
def map_view(request):
    return render(request, "location/map.html", {
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY
    })


@login_required
@require_POST
def save_address(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    address = data.get("address")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    label = data.get("label", "").strip()
    cliente_id = data.get("cliente_id")

    if not (address and latitude and longitude and cliente_id):
        return JsonResponse({"error": "Datos incompletos"}, status=400)

    try:
        addr = Address.objects.create(
            user=request.user,
            cliente_id=cliente_id,
            address=address,
            latitude=latitude,
            longitude=longitude,
            label=label
        )
    except Exception as e:
        return JsonResponse({"error": f"Error al guardar: {str(e)}"}, status=500)

    return JsonResponse({
        "id": addr.id,
        "address": addr.address,
        "label": addr.label
    })

class DireccionListView(ListView):
    model = Address
    template_name = "locations/direcciones_list.html"

class DireccionCreateView(CreateView):
    model = Address
    fields = ['linea1', 'linea2', 'ciudad', 'provincia', 'pais', 'codigo_postal', 'lat', 'lng', 'google_place_id']
    template_name = "core/form.html"
    success_url = reverse_lazy('direccion_list')
    extra_context = {"titulo": "Nueva Dirección"}
