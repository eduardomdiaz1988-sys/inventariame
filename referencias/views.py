from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Referencia, Tipo
from .forms import ReferenciaForm, TipoForm

# TIPOS
@login_required
def tipo_list(request):
    tipos = Tipo.objects.all()
    return render(request, "referencias/tipo_list.html", {"tipos": tipos})

@login_required
def tipo_nuevo(request):
    form = TipoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("tipo_list")
    return render(request, "referencias/tipo_form.html", {"form": form})

@login_required
def tipo_editar(request, pk):
    tipo = get_object_or_404(Tipo, pk=pk)
    form = TipoForm(request.POST or None, instance=tipo)
    if form.is_valid():
        form.save()
        return redirect("tipo_list")
    return render(request, "referencias/tipo_form.html", {"form": form})

@login_required
def tipo_eliminar(request, pk):
    tipo = get_object_or_404(Tipo, pk=pk)
    tipo.delete()
    return redirect("tipo_list")

# REFERENCIAS
@login_required
def referencia_list(request):
    referencias = Referencia.objects.select_related("tipo").all()
    return render(request, "referencias/referencia_list.html", {"referencias": referencias})

@login_required
def referencia_nuevo(request):
    form = ReferenciaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("referencia_list")
    return render(request, "referencias/referencia_form.html", {"form": form})

@login_required
def referencia_editar(request, pk):
    referencia = get_object_or_404(Referencia, pk=pk)
    form = ReferenciaForm(request.POST or None, instance=referencia)
    if form.is_valid():
        form.save()
        return redirect("referencia_list")
    return render(request, "referencias/referencia_form.html", {"form": form})

@login_required
def referencia_eliminar(request, pk):
    referencia = get_object_or_404(Referencia, pk=pk)
    referencia.delete()
    return redirect("referencia_list")
