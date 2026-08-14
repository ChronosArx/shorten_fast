from rest_framework import serializers
from apps.links.models import Link


class ShortLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = "__all__"
        read_only_fields = ["short_url", "code", "user"]
