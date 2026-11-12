from rest_framework import serializers
from apps.links.models import Link


class ShortLinkSerializer(serializers.ModelSerializer):
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


class QRCodeRequestSerializer(serializers.Serializer):
    original_url = serializers.URLField()
