from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Elemento, Stock, Cantidad
from users.mixins import GroupVisibilityMixin, SameOwnerRequiredMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.contrib import messages

from django.http import JsonResponse


def api_buscar_elemento(request):
    nombre = request.GET.get("nombre", "").lower()
    elemento = Elemento.objects.filter(nombre__iexact=nombre).first()
    if elemento:
        return JsonResponse({"id": elemento.id, "nombre": elemento.nombre})
    return JsonResponse({"error": "No encontrado"}, status=404)



class ElementoListView(LoginRequiredMixin, ListView):
    model = Elemento
    template_name = "inventory/elementos_list.html"

    def get_queryset(self):
        # Filtramos elementos que tengan cantidades asociadas al usuario
        return Elemento.objects.filter(cantidades__usuario=self.request.user).distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Diccionario con cantidades por elemento para el usuario
        cantidades = Cantidad.objects.filter(usuario=self.request.user)
        ctx["cantidades_dict"] = {c.elemento_id: c.cantidad for c in cantidades}
        return ctx


class ElementoCreateView(GroupVisibilityMixin, CreateView):
    model = Elemento
    fields = ['nombre', 'estado', 'tipo_identificador']
    template_name = "core/form.html"
    success_url = reverse_lazy('elemento_list')
    extra_context = {"titulo": "Nuevo Elemento"}

# --- Vista para editar Elementos ---
class ElementoUpdateView(LoginRequiredMixin, UpdateView):
    model = Elemento
    fields = ["nombre", "estado", "tipo_identificador"]
    template_name = "inventory/form.html"
    success_url = reverse_lazy("elemento_list")

    def get_queryset(self):
        # Solo permite editar elementos que estén asociados al usuario mediante Cantidad
        return Elemento.objects.filter(cantidades__usuario=self.request.user).distinct()
    
class ElementoDeleteView(GroupVisibilityMixin, DeleteView):
    model = Elemento
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy('elemento_list')
    extra_context = {"titulo": "Eliminar Elemento"}

class StockListView(GroupVisibilityMixin, ListView):
    model = Stock
    template_name = "inventory/stocks_list.html"

class StockCreateView(GroupVisibilityMixin, CreateView):
    model = Stock
    fields = ['elemento', 'codigo_is', 'nombre']
    template_name = "core/form.html"
    success_url = reverse_lazy('stock_list')
    extra_context = {"titulo": "Nuevo Stock"}

    def form_valid(self, form):
        # El stock lo crea el jefe de equipo; se asocia a su usuario
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class StockUpdateView(SameOwnerRequiredMixin, UpdateView):
    model = Stock
    fields = ['elemento', 'codigo_is', 'nombre']
    template_name = "core/form.html"
    success_url = reverse_lazy('stock_list')
    extra_context = {"titulo": "Editar Stock"}

class StockDeleteView(SameOwnerRequiredMixin, DeleteView):
    model = Stock
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy('stock_list')
    extra_context = {"titulo": "Eliminar Stock"}

class CantidadListView(GroupVisibilityMixin, ListView):
    model = Cantidad
    template_name = "inventory/cantidades_list.html"
    # inventory/views.py (en CantidadListView)
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from .models import Elemento
        ctx["elementos"] = Elemento.objects.order_by('nombre')
        return ctx


class CantidadCreateView(LoginRequiredMixin, CreateView):
    model = Cantidad
    fields = ['elemento', 'cantidad']
    template_name = "core/form.html"
    success_url = reverse_lazy('cantidad_list')
    extra_context = {"titulo": "Nueva Cantidad"}

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

# --- Vista para editar Cantidades ---
class CantidadUpdateView(LoginRequiredMixin, UpdateView):
    model = Cantidad
    fields = ["cantidad"]
    template_name = "inventory/form.html"
    success_url = reverse_lazy("cantidad_list")

    def get_queryset(self):
        # Solo permite editar las cantidades del usuario actual
        return Cantidad.objects.filter(usuario=self.request.user)
    
    
class CantidadDeleteView(SameOwnerRequiredMixin, DeleteView):
    model = Cantidad
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy('cantidad_list')
    extra_context = {"titulo": "Eliminar Cantidad"}

# Gestión de stock de usuario: sumar/restar/quitar items
class CantidadAdjustView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        elemento_id = request.POST.get('elemento_id')
        delta = int(request.POST.get('delta', 0))  # puede ser +1, -1, +N, -N
        try:
            cantidad, _ = Cantidad.objects.get_or_create(usuario=request.user, elemento_id=elemento_id, defaults={'cantidad': 0})
            nueva = cantidad.cantidad + delta
            if nueva < 0:
                messages.error(request, "No puedes tener cantidad negativa.")
            else:
                cantidad.cantidad = nueva
                cantidad.save()
                messages.success(request, f"Cantidad actualizada: {cantidad.cantidad}")
        except Elemento.DoesNotExist:
            messages.error(request, "Elemento no existe.")
        return redirect('cantidad_list')
    
