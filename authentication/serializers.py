from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserLogInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=250)
    password = serializers.CharField(write_only=True)


class ConfirmCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
