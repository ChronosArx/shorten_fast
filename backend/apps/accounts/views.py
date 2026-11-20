from typing import Any, cast

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .cookies import clear_refresh_cookie, get_refresh_cookie, set_refresh_cookie
from .serializers import (
    TokenObtainPairResponseSerializer,
    TokenPairResponseSerializer,
    TokenRefreshResponseSerializer,
    UserRegisterSerializer,
)

REFRESH_COOKIE_AUTH = cast(list[str], [{"refreshCookie": []}])


class Register(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    @extend_schema(
        tags=["Auth"],
        summary="Registro de nuevo usuario",
        description=(
            "Crea una cuenta en la plataforma. Devuelve el access token en el "
            "cuerpo de la respuesta y el refresh token en una cookie HttpOnly."
        ),
        responses={status.HTTP_201_CREATED: TokenPairResponseSerializer},
        auth=[],
    )
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:

        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        refresh_token = RefreshToken.for_user(user)

        response_data = {
            "access": str(refresh_token.access_token),
            "token_type": "Bearer",
        }

        response = Response(
            data=response_data,
            status=status.HTTP_201_CREATED,
        )
        set_refresh_cookie(response, str(refresh_token))
        return response


class LogoutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        tags=["Auth"],
        summary="Cerrar sesión",
        description=(
            "Toma el refresh token de la cookie HttpOnly, lo revoca para que no "
            "pueda volver a usarse y elimina la cookie."
        ),
        request=None,
        auth=REFRESH_COOKIE_AUTH,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Refresh token revocado correctamente."
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Refresh token inexistente, inválido o ya revocado."
            ),
        },
    )
    def post(self, request: Request) -> Response:
        refresh_token = get_refresh_cookie(request)

        if not refresh_token:
            response = Response(
                {"detail": "No se encontró el refresh token en la cookie."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            clear_refresh_cookie(response)
            return response

        try:
            RefreshToken(refresh_token).blacklist()  # type: ignore[arg-type]
        except TokenError:
            response = Response(
                {"detail": "Refresh token inválido o ya revocado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            response = Response(
                {"detail": "Sesión cerrada correctamente."},
                status=status.HTTP_200_OK,
            )

        clear_refresh_cookie(response)
        return response


@extend_schema(
    tags=["Auth"],
    auth=[],
    summary="Iniciar sesión",
    description=(
        "Autentica con email y contraseña. Devuelve el access token en el cuerpo "
        "de la respuesta y el refresh token en una cookie HttpOnly."
    ),
    responses={status.HTTP_200_OK: TokenObtainPairResponseSerializer},
)
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e

        refresh_token = serializer.validated_data.pop("refresh")
        serializer.validated_data["token_type"] = "Bearer"

        response = Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )
        set_refresh_cookie(response, refresh_token)
        return response


@extend_schema(
    tags=["Auth"],
    auth=REFRESH_COOKIE_AUTH,
    summary="Renovar token de acceso",
    description=(
        "Toma el refresh token de la cookie HttpOnly y devuelve un nuevo access "
        "token en el cuerpo de la respuesta. El refresh token no se rota."
    ),
    request=None,
    responses={
        status.HTTP_200_OK: TokenRefreshResponseSerializer,
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            description="Refresh token inexistente, inválido, expirado o revocado."
        ),
    },
)
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        refresh_token = get_refresh_cookie(request)

        if not refresh_token:
            return Response(
                {
                    "detail": "No se encontró el refresh token en la cookie.",
                    "code": "token_not_valid",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = TokenRefreshSerializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            response = Response(
                {
                    "detail": e.args[0] if e.args else "Refresh token inválido.",
                    "code": "token_not_valid",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
            clear_refresh_cookie(response)
            return response

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
