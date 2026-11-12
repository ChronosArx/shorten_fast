from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
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
