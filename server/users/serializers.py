from rest_framework import serializers

from .models import TokensTable, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
        ]


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password'
        ]


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokensTable
        fields = [
            'userid',
            'resetToken',
        ]
