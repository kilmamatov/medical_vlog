from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from . import serializers
from . import models
from .models import UserModel


class RegisterUser(GenericAPIView):
    queryset = UserModel
    serializer_class = serializers.RegisterUser

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserModel.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        token = Token.objects.create(user=user)
        return Response({'token': token.key})


class LoginUser(GenericAPIView):
    queryset = UserModel
    serializer_class = serializers.LoginUser

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = Token.objects.get(user__username=serializer.validated_data['username'])
        return Response({'token': token.key})

