from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
import re

from .models import User


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if not re.match('^[\w.@+-]+\Z', value) or value == 'me':
            raise serializers.ValidationError('Некорректный ввод username')
        return value


class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')

    def validate_username(self, value):
        if not re.match('^[\w.@+-]+\Z', value) or value == 'me':
            raise serializers.ValidationError('Некорректный ввод username')
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio',)

    def validate_username(self, value):
        if not re.match('^[\w.@+-]+\Z', value) or value == 'me':
            raise serializers.ValidationError('Некорректный ввод username')
        return value


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.name
        token['confirmation_code'] = user.confirmation_code

        return token
