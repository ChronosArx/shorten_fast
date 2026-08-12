from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import UserRegisterSerializer
from ..docs import response_access_token


@extend_schema(tags=["Authentication"], request=UserRegisterSerializer, auth=[])
class Register(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Este endpoint recibe un usario, contraseña y correo electrónico para poder hacer el registro en la plataforma.\n\n"
        "De igual manera al completar el registro retornara un access token y un refresh token el cual irá en una cookie"
        "este último para poder obtener nuevos tokens de acceso.",
        responses={status.HTTP_201_CREATED: response_access_token},
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
