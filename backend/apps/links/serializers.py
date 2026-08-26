from django.utils import timezone
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
            "user",
            "expires_at",
        ]
        read_only_fields = ["id", "short_url", "code", "user"]

    def validate_expires_at(self, value):
        if value and value <= timezone.now():
            raise serializers.ValidationError("La fecha de expiración debe ser futura.")
        return value

    def validate(self, attrs):
        if "expires_at" in attrs and self.context["request"].user.is_anonymous:
            del attrs["expires_at"]
        return attrs
