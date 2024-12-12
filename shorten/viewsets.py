from django.http.response import FileResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiParameter,
)
from .serializers import ShortLinkCreateSerializer, ShortLinkSerializer
from .models import ShortLink
from .utils import generate_short_code, generate_short_url
from .services import generate_qr
from .permissions import IsAuthenticatedOrCreate
from .mixins import CreateSerializerMixin


id_param = OpenApiParameter(
    name="id",
    type=int,
    location="path",
    description="ID del ShortLink",
    required=True,
)


@extend_schema_view(
    create=extend_schema(
        description="Solo los usuarios registrados pueden enviar un titulo para la creación del link acortado.",
        responses=ShortLinkSerializer,
    ),
    retrieve=extend_schema(
        description="Para obtener los detalles de un link en específico se necesita el id como parámetro.",
        parameters=[id_param],
    ),
    update=extend_schema(
        description="Para actualizar de un link en específico se necesita el id como parámetro y los datos a actualizar.",
        parameters=[id_param],
    ),
    destroy=extend_schema(
        description="Para la eliminación de un link es necesario pasar el id como parámetro.",
        parameters=[id_param],
    ),
)
@extend_schema(tags=["Shortlink"])
class ShortLinkViewSet(
    CreateSerializerMixin,
    viewsets.ModelViewSet,
):
    serializer_class = ShortLinkSerializer
    create_serializer_class = ShortLinkCreateSerializer
    permission_classes = [IsAuthenticatedOrCreate]
    http_method_names = ["get", "post", "delete", "put"]

    def get_queryset(self):
        return ShortLink.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        code = generate_short_code()
        short_url = generate_short_url(code=code)
        if self.request.user.is_anonymous:
            serializer.save(code=code, short_url=short_url, user_id=None)
            return
        serializer.save(code=code, short_url=short_url, user_id=self.request.user)

    @extend_schema(
        description="Este endpoint regresa un código qr en formato png.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response={
                    "application/json": {
                        "type": "image/png",
                    }
                },
                description="Se creó exitosamente el código qr",
            )
        },
    )
    @action(methods=["POST"], url_path="get-qr", detail=False, url_name="get-qr")
    def get_qrcode(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            qrcode = generate_qr(serializer.validated_data["original_url"])
            return FileResponse(
                qrcode,
                content_type="image/png",
                as_attachment=True,
                filename="qr_code.png",
            )
