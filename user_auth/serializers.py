from django.contrib.auth import authenticate
from rest_framework import serializers
import models


class RegisterUser(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8)

    def validate_username(self, value):
        if models.User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Пользователь с таким именем уже есть')
        return value


class LoginUser(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8)

    # def validate_username(self, value):
    #     if not models.User.objects.filter(username=value).exists():
    #         raise serializers.ValidationError('Пользователь с таким именем не найден')
    #     return value
    #
    # def validate(self, attrs):
    #     user = models.User.objects.get(username=attrs['username'])
    #     if not user.check_password(attrs['password']):
    #         raise serializers.ValidationError({'password': 'Пароль не верный'})
    #     return attrs

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Неверный логин или пароль')

        attrs['user'] = user
        return attrs
