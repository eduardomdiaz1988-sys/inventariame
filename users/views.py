from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm
from django.shortcuts import render
from django.db.models import Q
from core.models import Cliente, Cita
from inventory.models import Elemento, Cantidad
from sales.models import Venta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.models import User

def verificar_usuario(request):
    username = request.GET.get("username", "")
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({"exists": exists})

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect("home")  # Redirige al home


@login_required
def home_view(request):
    perfil = getattr(request.user, 'perfil', None)
    grupo = perfil.grupo_django.name if (perfil and perfil.grupo_django) else 'SinGrupo'

    ahora = timezone.now()
    proximas = Cita.objects.filter(
        fecha__gte=ahora,
        fecha__lte=ahora + timedelta(days=7)
    ).order_by('fecha')[:5]

    clientes = Cliente.objects.order_by('nombre')[:10]
    clientes_total = Cliente.objects.count()
    elementos_activos = Elemento.objects.filter(estado='ACTIVO').count()
    stock_bajo = Cantidad.objects.filter(usuario=request.user, cantidad__lt=2).count()

    return render(request, "users/dashboard.html", {
        "grupo": grupo,
        "clientes_total": clientes_total,
        "proximas": proximas,
        "elementos_activos": elementos_activos,
        "stock_bajo": stock_bajo,
        "clientes": clientes,
    })

def buscar_view(request):
    q = request.GET.get("q", "").strip()
    resultados = {"clientes": [], "citas": [], "ventas": [], "elementos": []}

    if q:
        resultados["clientes"] = Cliente.objects.filter(Q(nombre__icontains=q))
        resultados["citas"] = Cita.objects.filter(Q(cliente__nombre__icontains=q))
        resultados["ventas"] = Venta.objects.filter(Q(referencia__icontains=q))
        resultados["elementos"] = Elemento.objects.filter(Q(nombre__icontains=q))

    return render(request, "users/buscar.html", {"q": q, "resultados": resultados})

def registro_view(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegistroForm()
    return render(request, "users/registro.html", {"form": form})
