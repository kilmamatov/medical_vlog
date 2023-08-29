from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_205_RESET_CONTENT,
)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from user_auth.models import UserModel
from user_auth.serializers import (
    RegisterUser,
    UserProfileSerializer,
)


class RegisterUserView(GenericAPIView):
    queryset = UserModel
    serializer_class = RegisterUser

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserModel.objects.create_user(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        user.is_active = True
        user.save()
        return Response(
            {"message": "You have successfully registered"},
            status=HTTP_201_CREATED,
        )


class UserModelView(GenericAPIView):
    queryset = UserModel
    serializer_class = UserProfileSerializer
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk):
        try:
            user = UserModel.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(
                {"message": "User does not exist, try again"},
                status=HTTP_404_NOT_FOUND,
            )
        for key, value in self.request.data.items():
            setattr(user, key, value)
        serializer = self.serializer_class(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        user.save()
        return Response(serializer.data, status=HTTP_200_OK)

    def delete(self, request, pk):
        try:
            user = UserModel.objects.get(pk=pk)
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
        username = self.request.data["username"]
        password = self.request.data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            if self.request.user.is_authenticated:
                response.data["user_id"] = self.request.user.id
                response.data["username"] = self.request.user.username
            else:
                return Response(
                    {"message": "wrong credentials, try again"},
                    status=HTTP_400_BAD_REQUEST,
                )
        return response


class LogoutUserView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        logout(self.request)
        token_to_black_list = request.data["refresh_token"]
        token = RefreshToken(token_to_black_list)
        token.blacklist()
        return Response(status=HTTP_204_NO_CONTENT)
