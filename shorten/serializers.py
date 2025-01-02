from rest_framework import serializers
from .models import ShortLink


class ShortLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortLink
        fields = "__all__"
        extra_kwargs = {
            "short_url": {"read_only": True},
            "code": {"read_only": True},
            "user_id": {"read_only": True},
        }
