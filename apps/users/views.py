from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import UserRegisterSerializer
from .docs import response_access_token


class Register(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Authentication"],
        summary="Registro de nuevo usuario",
        description="Crea una cuenta en la plataforma y devuelve los tokens JWT iniciales para autenticación.",
        responses={status.HTTP_201_CREATED: response_access_token},
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


@extend_schema(tags=["Authentication"], auth=[])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=["Authentication"], auth=[])
class CustomTokenRefreshView(TokenRefreshView):
    pass
