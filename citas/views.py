from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from citas.forms import CitaForm, CitaWithClientForm
from clientes.models import Cliente
from locations.models import Address
from .models import Cita, CitaOferta
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from oferta.models import Oferta
from django.shortcuts import redirect, render, get_object_or_404


def cita_cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk, usuario=request.user)
    citas = Cita.objects.filter(cliente=cliente, usuario=request.user).order_by("fecha")
    return render(request, "citas/cita_detail.html", {
        "cliente": cliente,
        "citas": citas,
    })

class CitaListView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = "citas/citas_list.html"
    context_object_name = "object_list"

    def get_queryset(self):
        return (
            Cita.objects
            .select_related("cliente", "usuario")
            .prefetch_related("cita_ofertas__oferta")
        )

class CitaDetailView(LoginRequiredMixin, DetailView):
    model = Cita
    template_name = "citas/cita_detail.html"
    context_object_name = "cita"

    def get_queryset(self):
        # ✅ Solo citas del usuario autenticado
        return Cita.objects.filter(usuario=self.request.user)

class CitaCreateWithClientView(LoginRequiredMixin, CreateView):
    model = Cita
    form_class = CitaWithClientForm
    template_name = "citas/card_form/cita_form.html"
    success_url = reverse_lazy('cita_list')
    extra_context = {"titulo": "Nueva Cita"}

    def form_invalid(self, form):
        print("Errores en el formulario:", form.errors)
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        print("POST recibido:", request.POST)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # valores por defecto
        form.instance.recordatorio = False
        form.instance.estado = "pendiente"

        cliente_id = self.request.POST.get("cliente")
        nombre = self.request.POST.get("nombre", "").strip()
        telefono = self.request.POST.get("telefono", "").strip()
        address = self.request.POST.get("address", "").strip()
        latitude = self.request.POST.get("latitude")
        longitude = self.request.POST.get("longitude")
        label = self.request.POST.get("label", "").strip()

        cliente = None

        # caso: cliente nuevo
        if not cliente_id and nombre:
            cliente = Cliente.objects.create(
                nombre=nombre,
                telefono=telefono if telefono else None,
                usuario=self.request.user
            )
            if address and latitude and longitude:
                try:
                    direccion_obj = Address.objects.create(
                        user=self.request.user,
                        cliente=cliente,
                        address=address,
                        latitude=float(latitude),
                        longitude=float(longitude),
                        label=label if label else None,
                        principal=True
                    )
                    cliente.direccion = direccion_obj
                    cliente.save()
                except Exception as e:
                    form.add_error(None, f"Error creando dirección: {e}")
                    return self.form_invalid(form)

        # caso: cliente existente
        elif cliente_id:
            try:
                cliente = Cliente.objects.get(pk=cliente_id)
            except Cliente.DoesNotExist:
                form.add_error("cliente", "El cliente seleccionado no existe")
                return self.form_invalid(form)

        if not cliente:
            form.add_error("cliente", "Debes seleccionar o crear un cliente")
            return self.form_invalid(form)

        # asignamos cliente y usuario
        form.instance.cliente = cliente
        form.instance.usuario = self.request.user

        # Guardamos la cita primero
        cita = form.save()

        # ================================
        #   PROCESAR OFERTAS MÚLTIPLES
        # ================================
        ofertas_ids = self.request.POST.getlist("ofertas[]")
        cantidades = self.request.POST.getlist("cantidad[]")

        for oferta_id, cantidad in zip(ofertas_ids, cantidades):
            try:
                oferta = Oferta.objects.get(pk=oferta_id)
                cantidad_int = int(cantidad)

                CitaOferta.objects.create(
                    cita=cita,
                    oferta=oferta,
                    cantidad=cantidad_int
                )
            except Exception as e:
                form.add_error(None, f"Error procesando oferta {oferta_id}: {e}")
                return self.form_invalid(form)

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["GOOGLE_MAPS_API_KEY"] = settings.GOOGLE_MAPS_API_KEY
        return context


class CitaCreateView(LoginRequiredMixin, CreateView):
    model = Cita
    form_class = CitaForm
    template_name = "citas/cita_form.html"
    success_url = reverse_lazy('cita_list')
    extra_context = {"titulo": "Nueva Cita"}

    def form_valid(self, form):
        # Guardar la cita
        cita = form.save(commit=False)
        cita.usuario = self.request.user
        cita.save()

        # Procesar ofertas múltiples
        ofertas_ids = self.request.POST.getlist("ofertas")
        cantidades = self.request.POST.getlist("cantidad")

        for oferta_id, cantidad in zip(ofertas_ids, cantidades):
            CitaOferta.objects.create(
                cita=cita,
                oferta_id=int(oferta_id),
                cantidad=int(cantidad)
            )

        return redirect(self.success_url)
    
class CitaUpdateView(LoginRequiredMixin, UpdateView):
    model = Cita
    form_class = CitaForm
    template_name = "citas/cita_form.html"
    success_url = reverse_lazy('cita_list')
    extra_context = {"titulo": "Editar Cita"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ofertas_existentes"] = self.object.cita_ofertas.select_related("oferta").all()
        return context
    
    def form_invalid(self, form):
        print("\n❌ FORM INVALID ❌")
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.cliente = self.object.cliente
        cita = form.save(commit=False)
        cita.save()

        # Leer listas correctamente
        ofertas_ids = self.request.POST.getlist("ofertas")
        cantidades = self.request.POST.getlist("cantidad")

        print("\n========== DEBUG ==========")
        print("POST:", dict(self.request.POST))
        print("Ofertas:", ofertas_ids)
        print("Cantidades:", cantidades)
        print("===========================\n")

        # Borrar ofertas anteriores
        cita.cita_ofertas.all().delete()

        # Crear nuevas
        for oferta_id, cantidad in zip(ofertas_ids, cantidades):
            print(f"Guardando oferta {oferta_id} x {cantidad}")
            CitaOferta.objects.create(
                cita=cita,
                oferta_id=int(oferta_id),
                cantidad=int(cantidad)
            )

        return redirect(self.success_url)





class CitaDeleteView(LoginRequiredMixin, DeleteView):
    model = Cita
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy('cita_list')
    extra_context = {"titulo": "Eliminar Cita"}

@login_required
def buscar_ofertas(request):
    q = request.GET.get("q", "").strip()
    resultados = []
    if q:
        ofertas = Oferta.objects.filter(nombre__icontains=q)[:10]  # límite de resultados
        resultados = [{"id": o.id, "nombre": o.nombre, "valor": o.valor} for o in ofertas]
    return JsonResponse(resultados, safe=False)