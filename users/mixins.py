# users/mixins.py
from django.contrib.auth.models import Group
from django.core.exceptions import ImproperlyConfigured
# users/mixins.py
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied

class GroupVisibilityMixin:
    """
    Filtra el queryset para que:
    - Usuarios individuales vean solo sus objetos.
    - Usuarios de grupo vean los objetos de todos los miembros de su grupo.
    Requiere que el modelo tenga un campo 'usuario'.
    """
    owner_field_name = "usuario"

    def get_queryset(self):
        qs = super().get_queryset()
        perfil = getattr(self.request.user, "perfil", None)
        if not perfil:
            return qs.none()

        if perfil.tipo_usuario == "grupo" and perfil.grupo_django:
            return qs.filter(**{f"{self.owner_field_name}__groups": perfil.grupo_django})
        return qs.filter(**{self.owner_field_name: self.request.user})


class SameOwnerRequiredMixin:
    """
    Restringe acceso a objetos:
    - Solo el propietario o alguien del mismo grupo puede acceder.
    """
    owner_field_name = "usuario"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        perfil = getattr(request.user, "perfil", None)

        if not perfil:
            raise PermissionDenied

        if perfil.tipo_usuario == "grupo" and perfil.grupo_django:
            if obj.usuario.groups.filter(id=perfil.grupo_django.id).exists():
                return super().dispatch(request, *args, **kwargs)
        elif obj.usuario == request.user:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied

class LoginRequiredMixin(AccessMixin):
    """Redirige a login si el usuario no está autenticado."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class OwnerQuerySetMixin:
    """
    Filtra el queryset en función del perfil del usuario:
    - Individual: usuario == request.user
    - Grupo: usuario__groups contiene el grupo del perfil (perfil.grupo_django)
    Requiere que el modelo tenga un campo 'usuario' (FK a User).
    """
    owner_field_name = "usuario"  # permite cambiarlo si tu modelo usa otro nombre

    def get_owner_group(self):
        perfil = getattr(self.request.user, "perfil", None)
        return getattr(perfil, "grupo_django", None)

    def filter_for_owner(self, qs):
        perfil = getattr(self.request.user, "perfil", None)
        if not perfil:
            # Sin perfil, por seguridad no devuelve datos
            return qs.none()

        if perfil.tipo_usuario == "grupo" and perfil.grupo_django:
            return qs.filter(**{f"{self.owner_field_name}__groups": perfil.grupo_django})
        # Individual por defecto
        return qs.filter(**{self.owner_field_name: self.request.user})

    def get_queryset(self):
        qs = super().get_queryset()
        if self.owner_field_name is None:
            raise ImproperlyConfigured("Debes definir owner_field_name en OwnerQuerySetMixin")
        return self.filter_for_owner(qs)


# users/mixins.py (añade esto también)
class OwnerCreateMixin:
    """
    Asigna request.user al campo 'usuario' al crear objetos.
    Úsalo en CreateView y en ModelFormMixin.
    """
    owner_field_name = "usuario"

    def form_valid(self, form):
        setattr(form.instance, self.owner_field_name, self.request.user)
        return super().form_valid(form)
