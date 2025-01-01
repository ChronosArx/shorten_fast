from rest_framework.permissions import BasePermission


class IsAuthenticatedOrCreate(BasePermission):
    """
    Permiso que permite a cualquier usuario realizar una acción de creación
    sin autenticación, pero requiere autenticación para otras acciones.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return request.user.is_authenticated
