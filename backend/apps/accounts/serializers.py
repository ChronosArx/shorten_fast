from typing import Any

from rest_framework import serializers

from apps.accounts.models import User


class UserRegisterSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data: Any) -> User:
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


# Response Schemas


class TokenPairResponseSerializer(serializers.Serializer[Any]):
    access = serializers.CharField()
    token_type = serializers.CharField()


class TokenObtainPairResponseSerializer(serializers.Serializer[Any]):
    access = serializers.CharField()
    token_type = serializers.CharField()


class TokenRefreshResponseSerializer(serializers.Serializer[Any]):
    access = serializers.CharField()
