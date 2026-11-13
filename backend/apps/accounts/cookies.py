from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings


def get_refresh_cookie(request: Request) -> str | None:
    """Devuelve el refresh token almacenado en la cookie o ``None``."""
    return request.COOKIES.get(settings.AUTH_REFRESH_COOKIE_NAME)


def set_refresh_cookie(response: Response, refresh_token: str) -> None:
    """Guarda el refresh token en una cookie HttpOnly de la respuesta."""
    response.set_cookie(
        key=settings.AUTH_REFRESH_COOKIE_NAME,
        value=refresh_token,
        max_age=int(api_settings.REFRESH_TOKEN_LIFETIME.total_seconds()),
        httponly=True,
        secure=settings.AUTH_REFRESH_COOKIE_SECURE,
        samesite=settings.AUTH_REFRESH_COOKIE_SAMESITE,
        path=settings.AUTH_REFRESH_COOKIE_PATH,
    )


def clear_refresh_cookie(response: Response) -> None:
    """Elimina la cookie del refresh token del navegador."""
    response.delete_cookie(
        key=settings.AUTH_REFRESH_COOKIE_NAME,
        path=settings.AUTH_REFRESH_COOKIE_PATH,
        samesite=settings.AUTH_REFRESH_COOKIE_SAMESITE,
    )
