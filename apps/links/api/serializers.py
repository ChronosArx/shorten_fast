from rest_framework import serializers
from ..models import ShortLink


class ShortLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortLink
        fields = "__all__"
        read_only_fields = ["short_url", "code", "user"]
