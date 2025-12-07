from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegistroForm
from django.db.models import Q
from core.models import Cliente, Cita
from inventory.models import Elemento, Cantidad
from sales.models import Venta
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from .models import PerfilUsuario
from users.utils import qs_for_request_user

def registro_view(request):
    if request.method == "POST":
        tipo_usuario = request.POST.get("tipo_usuario", "individual")
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(tipo_usuario=tipo_usuario)
            login(request, user)
            return redirect("home")
    else:
        form = RegistroForm()
    return render(request, "users/registro.html", {"form": form})

def verificar_usuario(request):
    username = request.GET.get("username", "")
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({"exists": exists})

def logout_view(request):
    logout(request)
    return redirect("home")



@login_required
def home_view(request):
    perfil = getattr(request.user, "perfil", None)

    if perfil and perfil.tipo_usuario == "grupo":
        grupo = perfil.grupo_django
        clientes_qs = Cliente.objects.filter(usuario__groups=grupo)
        citas_qs = Cita.objects.filter(usuario__groups=grupo, fecha__gte=timezone.now())
        elementos_qs = Elemento.objects.filter(usuario__groups=grupo, estado="BUENO")
        stock_qs = Cantidad.objects.filter(usuario__groups=grupo, cantidad__lt=2)
    else:
        clientes_qs = Cliente.objects.filter(usuario=request.user)
        citas_qs = Cita.objects.filter(usuario=request.user, fecha__gte=timezone.now())
        elementos_qs = Elemento.objects.filter(usuario=request.user, estado="BUENO")
        stock_qs = Cantidad.objects.filter(usuario=request.user, cantidad__lt=2)

    context = {
        "clientes_total": clientes_qs.count(),
        "proximas": citas_qs.order_by("fecha")[:5],
        "citas_total": citas_qs.count(),
        "elementos_activos": elementos_qs.count(),
        "stock_bajo": stock_qs.count(),
        "clientes": clientes_qs.order_by("nombre")[:10],
    }

    return render(request, "users/dashboard.html", context)

def buscar_view(request):
    q = request.GET.get("q", "").strip()
    resultados = {"clientes": [], "citas": [], "ventas": [], "elementos": []}

    if q:
        resultados["clientes"] = Cliente.objects.filter(Q(nombre__icontains=q))
        resultados["citas"] = Cita.objects.filter(Q(cliente__nombre__icontains=q))
        resultados["ventas"] = Venta.objects.filter(Q(referencia__icontains=q))
        resultados["elementos"] = Elemento.objects.filter(Q(nombre__icontains=q))

    return render(request, "users/buscar.html", {"q": q, "resultados": resultados})

