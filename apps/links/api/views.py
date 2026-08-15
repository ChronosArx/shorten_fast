from typing import Any, cast

from django.http.response import FileResponse
from django.shortcuts import redirect
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from .serializers import ShortLinkSerializer
from apps.links.models import Link
from apps.links.services import (
    generate_qr,
    create_short_link,
    get_original_url_and_increment_click,
)
from .permissions import IsAuthenticatedOrCreate
from apps.users.models import User


@extend_schema(
    description="Este es el punto de entrada para redirigir todos los links acortados.",
    tags=["Redirects"],
    auth=[],
    request=None,
    responses={
        status.HTTP_302_FOUND: OpenApiResponse(
            description="Redirección exitosa al link original"
        ),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            description="No se encontró el link acortado"
        ),
    },
)
class Redirects(APIView):
    permission_classes = [AllowAny]

    def get(self, request, code):
        original_url = get_original_url_and_increment_click(code=code)

        if not original_url:
            return Response(
                {"detail": "Page not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        return redirect(original_url)


@extend_schema(tags=["Shortlink"])
class ShortLinkViewSet(
    viewsets.ModelViewSet,
):
    serializer_class = ShortLinkSerializer
    permission_classes = [IsAuthenticatedOrCreate]
    http_method_names = ["get", "post", "delete", "put"]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Link.objects.none()
        return Link.objects.filter(user=user)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        original_url = serializer.validated_data["original_url"]
        title = serializer.validated_data.get("title")
        user = cast(User, request.user) if request.user.is_authenticated else None
        link = create_short_link(title=title, original_url=original_url, user=user)
        serializer = self.get_serializer(link)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        description="Genera un código QR PNG a partir de una URL.",
    )
    @action(methods=["POST"], url_path="get-qr", detail=False, url_name="get-qr")
    def get_qrcode(self, request) -> FileResponse:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        qrcode = generate_qr(serializer.validated_data["original_url"])
        return FileResponse(
            qrcode,
            content_type="image/png",
            as_attachment=True,
            filename="qr_code.png",
        )
