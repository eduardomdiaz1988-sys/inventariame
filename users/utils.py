# users/utils.py
def qs_for_request_user(qs, request, owner_field_name="usuario"):
    perfil = getattr(request.user, "perfil", None)
    if not perfil:
        return qs.none()

    if perfil.tipo_usuario == "grupo" and perfil.grupo_django:
        return qs.filter(**{f"{owner_field_name}__groups": perfil.grupo_django})
    return qs.filter(**{owner_field_name: request.user})
