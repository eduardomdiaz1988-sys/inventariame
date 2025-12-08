from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Oferta
from .forms import OfertaForm

@login_required
def oferta_list(request):
    ofertas = Oferta.objects.select_related("referencia", "referencia__tipo").all()
    return render(request, "oferta/oferta_list.html", {"ofertas": ofertas})

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
