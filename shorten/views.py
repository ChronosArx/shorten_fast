from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from django.shortcuts import redirect
from shorten.models import ShortLink


# Create your views here.
@extend_schema(
    description="Este es el punto de entrada para redirigir todos los links acortados.",
    tags=["Redirects"],
    auth=[],
)
class Redirects(APIView):
    queryset = ShortLink.objects.all()
    serializer_class = None
    permission_classes = [AllowAny]

    def get(self, request, code):
        shortLink = self.queryset.filter(code=code).first()
        if shortLink:
            original_url = shortLink.original_url
            return redirect(original_url)
        else:
            return Response(
                {"detail": "Page not Found"}, status=status.HTTP_404_NOT_FOUND
            )
