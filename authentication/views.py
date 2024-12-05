from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from .serializers import UserRegisterSerializer, UserLogInSerializer, EmptySerializer


response_acccess_token = OpenApiResponse(
    response=OpenApiTypes.OBJECT,
    description="Retorna el token de acceso",
    examples=[
        OpenApiExample(
            name="access_token",
            value={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMDAwMDAwLCJpYXQiOjE2MDAwMDAwMDAsImp0aSI6IjEyMzQ1Njc4OTAiLCJ1c2VyX2lkIjoxfQ.n3IA6Of8g93IMV9G5u5ziN6ZtE6fWUcNu2Z6iHCjFWo",
            },
        )
    ],
)


# Create your views here.
@extend_schema(tags=["Authentication"], auth=[])
class Register(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        description="Este endpoint recibe un usario, contraseña y correo electrónico para poder hacer el registro en la plataforma.\n\n"
        "De igual manera al completar el registro retornara un access token y un refresh token el cual irá en una cookie"
        "este último para poder obtener nuevos tokens de acceso.",
        responses={status.HTTP_201_CREATED: response_acccess_token},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            access_token = AccessToken.for_user(user=user)
            refresh_token = RefreshToken.for_user(user=user)

            response = Response(
                {"access_token": str(access_token)}, status=status.HTTP_201_CREATED
            )

            response.set_cookie(
                key="refresh_token",
                value=str(refresh_token),
                httponly=True,
                samesite="Lax",
                secure=True,
            )

            return response


@extend_schema(tags=["Authentication"], auth=[])
class LogIn(generics.CreateAPIView):
    serializer_class = UserLogInSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        description="Este endpoint recibe usuario y contraseña para poder hacer login.\n\n"
        "De igual manera envía un token de acceso y un refresh token igual en cookies",
        responses={status.HTTP_200_OK: response_acccess_token},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                access_token = AccessToken.for_user(user=user)
                refresh_token = RefreshToken.for_user(user=user)

                response = Response(
                    {"access_token": str(access_token)}, status=status.HTTP_200_OK
                )

                response.set_cookie(
                    key="refresh_token",
                    value=str(refresh_token),
                    httponly=True,
                    samesite="Lax",
                    secure=True,
                )

                return response
            else:
                return Response(
                    {"error": "Credenciales inválidas"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )


@extend_schema(tags=["Authentication"], auth=[])
class LogOut(APIView):
    serializer_class = None
    permission_classes = [AllowAny]

    @extend_schema(
        description="Este endpoint elimina el refresh token del usuario de las cookies.\n\n"
        "El token de acceso deberá ser eliminado desde el frontend para evitar fallos de seguridad.",
        parameters=None,
        summary="Logout user",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Log Out Succesfull",
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        response = Response({"detail": "Log Out Successful"}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token")
        return response


@extend_schema(tags=["Authentication"], auth=[])
class GenerateAccesToken(APIView):
    serializer_class = None
    permission_classes = [AllowAny]

    @extend_schema(
        description="Este endpoint recibe el refresh token desde las cookies y retorna de respuesta un nuevo access token.",
        responses={status.HTTP_200_OK: response_acccess_token},
    )
    def get(self, request):
        try:
            token = request.COOKIES.get("refresh_token")

            if token is None:
                return Response(
                    {"detail": "Credentials Error!"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            token_data = RefreshToken(token=token)
            data = token_data.payload
            user = get_object_or_404(User, id=data["user_id"])
            access_token = AccessToken.for_user(user=user)
            return Response(
                {"access_token": str(access_token)}, status=status.HTTP_201_CREATED
            )
        except TokenError as e:
            return Response({"valid": False, "Error": str(e)})
