import os

import jwt
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from user_auth.models import UserModel
from user_auth.serializers import (
    EmailVerificationSerializer,
    RegisterUser,
    UserProfileSerializer,
)
from user_auth.utils import Supporting


class RegisterUserView(GenericAPIView):
    queryset = UserModel
    serializer_class = RegisterUser

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserModel.objects.create_user(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
            email=serializer.validated_data["email"],
        )
        user.save()
        Supporting.send_email(request, user)
        return Response(
            {
                "message": f"You have successfully registered, go to {user.email} and verify it",
            },
            status=HTTP_201_CREATED,
        )


class UserModelView(GenericAPIView):
    queryset = UserModel
    serializer_class = UserProfileSerializer
    parser_class = (FileUploadParser,)

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            user = UserModel.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(
                {"message": "User does not exist, try again"},
                status=HTTP_404_NOT_FOUND,
            )
        if self.request.user.pk == user.pk:
            for key, value in self.request.data.items():
                setattr(user, key, value)
            serializer = self.serializer_class(
                data=request.data,
                instance=user,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            user.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(
                {"message": "User does have permission for changed"},
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        try:
            user = UserModel.objects.get(pk=pk)
            if self.request.user.pk == user.pk:
                user.delete()
                return Response(
                    {"message": "User successfully deleted"},
                    status=HTTP_200_OK,
                )
        except ObjectDoesNotExist:
            return Response(
                {"message": "User does not exist, try again"},
                status=HTTP_404_NOT_FOUND,
            )


class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_authenticated:
                response.data["user_id"] = user.id
                response.data["username"] = user.username
                return response            
        return None


class LogoutUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(self.request)
        token_to_black_list = request.data["refresh_token"]
        token = RefreshToken(token_to_black_list)
        token.blacklist()
        return Response(status=HTTP_204_NO_CONTENT)


class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            user = UserModel.objects.get(id=payload["user_id"])
            if not user.is_verify_email or not user.is_active:
                user.is_verify_email = True
                user.is_active = True
                user.save()
            return Response(
                {
                    "email": "Successfully activated",
                },
                status=HTTP_200_OK,
            )
        except jwt.ExpiredSignatureError:
            return Response(
                {
                    "error": "Activation Expired",
                },
                status=HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {
                    "error": "Invalid token",
                },
                status=HTTP_400_BAD_REQUEST,
            )
