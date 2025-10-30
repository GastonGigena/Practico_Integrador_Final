def user_groups(request):
    """
    Devuelve la lista de nombres de grupos a los que pertenece el usuario logueado.
    Si no está logueado, devuelve lista vacía.
    """
    if request.user.is_authenticated:
        groups = list(request.user.groups.values_list('name', flat=True))
        return {'user_groups': groups}
    return {'user_groups': []}