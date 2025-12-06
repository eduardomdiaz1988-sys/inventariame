from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cliente
from .forms import ClienteForm
from locations.models import Address
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings




@login_required
@require_POST
def set_principal(request, pk):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    direccion_id = data.get("direccion_id")
    if not direccion_id:
        return JsonResponse({"error": "Falta direccion_id"}, status=400)

    try:
        cliente = Cliente.objects.get(pk=pk)
        direccion = Address.objects.get(pk=direccion_id, cliente=cliente)
        cliente.direccion = direccion
        cliente.save()
        return JsonResponse({
            "success": True,
            "direccion": direccion.address,
            "id": direccion.id
        })
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)
    except Address.DoesNotExist:
        return JsonResponse({"error": "Dirección no encontrada"}, status=404)
    
@login_required
def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, "clientes/cliente_list.html", {"clientes": clientes})

@login_required
def cliente_nuevo(request):
    cliente = None
    form = ClienteForm(request.POST or None, cliente=cliente)
    if form.is_valid():
        cliente = form.save(commit=False)
        cliente.save()
        return redirect("cliente_update", pk=cliente.pk)
    return render(request, "clientes/cliente_form.html", {
        "form": form,
        "cliente": cliente,
        "direcciones": [],
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
        "nuevo": True
    })

@login_required
def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    direcciones = Address.objects.filter(cliente=cliente)
    direccion_principal = cliente.direccion
    form = ClienteForm(request.POST or None, instance=cliente, cliente=cliente)
    if form.is_valid():
        form.save()
        return redirect("cliente_list")
    return render(request, "clientes/cliente_form.html", {
        "form": form,
        "cliente": cliente,
        "direcciones": direcciones,
        "direccion_principal": direccion_principal,
        "nuevo": False,
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY
    })

@login_required
def cliente_eliminar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.delete()
        return redirect("cliente_list")
    return render(request, "clientes/cliente_confirm_delete.html", {"cliente": cliente})
