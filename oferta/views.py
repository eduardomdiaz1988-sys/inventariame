# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from referencias.models import Tipo
from .models import Oferta
from .forms import OfertaForm
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
# oferta/views_api.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from oferta.models import Oferta
from django.db import models

@require_GET
@login_required
def buscar_ofertas(request):
    q = (request.GET.get("q") or "").strip()
    if not q:
        return JsonResponse([], safe=False)

    # Filtrar por nombre de oferta, referencia o tipo
    ofertas = Oferta.objects.filter(
        models.Q(nombre__icontains=q) |
        models.Q(referencia__nombre__icontains=q) |
        models.Q(referencia__tipo__nombre__icontains=q)
    ).select_related("referencia", "referencia__tipo")[:20]

    data = []
    for o in ofertas:
        tipo = o.referencia.tipo.nombre
        display = f"{o.nombre} - {o.referencia.nombre} - 0 + {o.valor}"

        data.append({
            "id": o.id,
            "nombre": display,
            "tipo": tipo,
            "valor": o.valor
        })

    return JsonResponse(data, safe=False)

@login_required
def oferta_list(request):
    qs = Oferta.objects.select_related("referencia", "referencia__tipo").all()

    nombre = request.GET.get("nombre", "").strip()
    referencia = request.GET.get("referencia", "").strip()
    tipo = request.GET.get("tipo", "").strip()
    valor = request.GET.get("valor", "").strip()

    if nombre:
        qs = qs.filter(nombre__icontains=nombre)
    if referencia:
        qs = qs.filter(referencia__nombre__icontains=referencia)
    if tipo:
        qs = qs.filter(referencia__tipo__nombre__icontains=tipo)
    if valor:
        qs = qs.filter(valor=valor)

    # ✅ lista de valores permitidos
    valores = [3, 4, 5, 7, 10]
    # ✅ obtenemos dinámicamente los tipos disponibles en la BD
    tipos = Tipo.objects.values_list("nombre", flat=True)
    
    return render(
        request,
        "oferta/oferta_list.html",
        {
            "ofertas": qs,
            "valores": valores,
            "tipos": tipos,
        },
    )

@login_required
def oferta_nueva(request):
    form = OfertaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("oferta_list")
    return render(request, "oferta/oferta_form.html", {"form": form, "titulo": "Nueva oferta"})

@login_required
def oferta_editar(request, pk):
    oferta = get_object_or_404(Oferta, pk=pk)
    form = OfertaForm(request.POST or None, instance=oferta)
    if form.is_valid():
        form.save()
        return redirect("oferta_list")
    return render(request, "oferta/oferta_form.html", {"form": form, "titulo": "Editar oferta"})

@login_required
def oferta_eliminar(request, pk):
    oferta = get_object_or_404(Oferta, pk=pk)
    if request.method == "POST":
        oferta.delete()
        return redirect("oferta_list")
    return render(request, "oferta/oferta_confirm_delete.html", {"oferta": oferta})

@login_required
def oferta_detail(request, pk):
    oferta = get_object_or_404(Oferta.objects.select_related("referencia", "referencia__tipo"), pk=pk)
    return render(request, "oferta/oferta_detail.html", {"oferta": oferta})
