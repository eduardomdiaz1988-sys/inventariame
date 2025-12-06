from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

class OwnerQuerysetMixin(LoginRequiredMixin):
    """
    Filtra el queryset por el usuario autenticado cuando el modelo tiene campo 'usuario'.
    """
    owner_field = 'usuario'

    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self.model, self.owner_field):
            return qs.filter(**{self.owner_field: self.request.user})
        return qs

class SameOwnerRequiredMixin(UserPassesTestMixin):
    """
    Restringe edición/borrado a propietario del objeto cuando tiene campo 'usuario'.
    """
    owner_field = 'usuario'

    def test_func(self):
        obj = self.get_object()
        return getattr(obj, self.owner_field) == self.request.user

class GroupVisibilityMixin(LoginRequiredMixin):
    """
    Los jefes de equipo pueden ver contenido de su grupo (grupo_django).
    Otros usuarios, solo su propio contenido.
    Requiere que el modelo tenga campo 'usuario'.
    """
    owner_field = 'usuario'

    def get_queryset(self):
        qs = super().get_queryset()
        perfil = getattr(self.request.user, 'perfil', None)
        if not perfil:
            return qs.none()
        # Si es Jefe de equipo, ver por grupo
        if perfil.grupo_django and perfil.grupo_django.name == 'JefeEquipo':
            user_ids = type(self.request.user).objects.filter(
                perfil__grupo_django=perfil.grupo_django
            ).values_list('id', flat=True)
            return qs.filter(**{f"{self.owner_field}__in": user_ids})
        # Usuarios normales: solo su contenido
        return qs.filter(**{self.owner_field: self.request.user})
