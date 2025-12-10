from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import List

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        # we do NOT expose `user` here, backend will set it
        fields = ["id", "title", "description", "status", "created_date"]
        read_only_fields = ["id", "created_date"]


class SignupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "name"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        name = validated_data.pop("name")
        password = validated_data.pop("password")
        username = validated_data.pop("username")

        user = User(
            username=username,
            first_name=name,
        )
        user.password = make_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
