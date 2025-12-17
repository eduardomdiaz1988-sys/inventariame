from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cliente
from .forms import ClienteForm, CitaWithClientForm
from locations.models import Address
import json
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.db.models import Q
from locations.models import Address

@require_GET
def buscar_cliente(request):
    q = request.GET.get("q", "").strip()
    resultados = []

    if q:
        clientes = Cliente.objects.filter(
            Q(nombre__icontains=q) | Q(telefono__icontains=q)
        )[:10]  # limita a 10 resultados
        resultados = [
            {"id": c.id, "nombre": c.nombre, "telefono": c.telefono}
            for c in clientes
        ]

    return JsonResponse(resultados, safe=False)


# --- AJAX para marcar dirección principal ---
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


# --- Listado de clientes ---
@login_required
def cliente_list(request):
    # ✅ Solo clientes del usuario autenticado
    clientes = Cliente.objects.filter(usuario=request.user)
    return render(request, "clientes/cliente_list.html", {"clientes": clientes})

# --- Crear cliente ---
@login_required
def cliente_nuevo(request):
    cliente = None
    form = ClienteForm(request.POST or None, cliente=cliente)
    if form.is_valid():
        cliente = form.save(commit=False)
        cliente.usuario = request.user
        cliente.save()
        return redirect("cliente_update", pk=cliente.pk)
    return render(request, "clientes/cliente_form.html", {
        "form": form,
        "cliente": cliente,
        "direcciones": [],
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
        "nuevo": True
    })


# --- Editar cliente ---
@login_required
def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    direcciones = Address.objects.filter(cliente=cliente)
    direccion_principal = cliente.direccion
    form = ClienteForm(request.POST or None, instance=cliente, cliente=cliente)

    if cliente.usuario != request.user:
        return HttpResponseForbidden("No tienes permiso para editar este cliente.")

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


# --- Eliminar cliente ---
@login_required
def cliente_eliminar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.delete()
        return redirect("cliente_list")
    return render(request, "clientes/cliente_confirm_delete.html", {"cliente": cliente})
