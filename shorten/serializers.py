from rest_framework import serializers
from .models import ShortLink


class ShortLinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortLink
        fields = ["title", "original_url"]


class ShortLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortLink
        fields = "__all__"
