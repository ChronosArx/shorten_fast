from typing import Any

from rest_framework import serializers
from apps.links.models import Link


class ShortLinkSerializer(serializers.ModelSerializer[Link]):
    class Meta:
        model = Link
        fields = [
            "id",
            "title",
            "short_url",
            "original_url",
            "code",
            "clicks",
            "user",
        ]
        read_only_fields = ["id", "short_url", "code", "clicks", "user"]


class QRCodeRequestSerializer(serializers.Serializer[Any]):
    original_url = serializers.URLField()
