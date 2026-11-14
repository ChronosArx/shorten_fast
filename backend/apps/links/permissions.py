from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAuthenticatedOrCreate(BasePermission):
    """
    Permiso que permite a cualquier usuario realizar una acción de creación
    sin autenticación, pero requiere autenticación para otras acciones.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method == "POST":
            return True
        return bool(request.user.is_authenticated)
