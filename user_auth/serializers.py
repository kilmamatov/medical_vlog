from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from core.models import Post
from .models import UserModel


class UserSerializer(serializers.ModelSerializer):
    post = Post

    class Meta:
        model = UserModel
        fields = ['nickname', 'photo', 'description', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        user = UserModel.objects.create(**validated_data)
        return user


class RegisterUser(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8)
    password_again = serializers.CharField(min_length=8)

    def validate_username(self, value):
        if UserModel.objects.filter(username=value).exists():
            raise serializers.ValidationError('Пользователь с таким именем уже есть')
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password_again = attrs.get('password_again')
        if password != password_again:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs


class LoginUser(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Неверный логин или пароль')

        attrs['user'] = user
        return attrs
