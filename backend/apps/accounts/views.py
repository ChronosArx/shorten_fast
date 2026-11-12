from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
    LogoutSerializer,
    TokenObtainPairResponseSerializer,
    TokenPairResponseSerializer,
    TokenRefreshResponseSerializer,
    UserRegisterSerializer,
)


class Register(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    @extend_schema(
        tags=["Auth"],
        summary="Registro de nuevo usuario",
        description="Crea una cuenta en la plataforma y devuelve los tokens JWT iniciales para autenticación.",
        responses={status.HTTP_201_CREATED: TokenPairResponseSerializer},
        auth=[],
    )
    def post(self, request, *args, **kwargs):

        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        refresh_token = RefreshToken.for_user(user)

        response_data = {
            "access": str(refresh_token.access_token),
            "refresh": str(refresh_token),
            "token_type": "Bearer",
        }

        return Response(
            data=response_data,
            status=status.HTTP_201_CREATED,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    @extend_schema(
        tags=["Auth"],
        summary="Cerrar sesión",
        description="Revoca el refresh token recibido para que no pueda volver a usarse.",
        request=LogoutSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Refresh token revocado correctamente."
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Refresh token inválido o ya revocado."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Se requiere autenticación."
            ),
        },
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            RefreshToken(serializer.validated_data["refresh"]).blacklist()
        except TokenError:
            return Response(
                {"detail": "Refresh token inválido o ya revocado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Sesión cerrada correctamente."},
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Auth"],
    auth=[],
    summary="Iniciar sesión",
    description="Autentica con email y contraseña y devuelve un par de tokens JWT.",
    responses={status.HTTP_200_OK: TokenObtainPairResponseSerializer},
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(
    tags=["Auth"],
    auth=[],
    summary="Renovar token de acceso",
    description="Devuelve un nuevo token de acceso a partir de un refresh token válido.",
    responses={status.HTTP_200_OK: TokenRefreshResponseSerializer},
)
class CustomTokenRefreshView(TokenRefreshView):
    pass
