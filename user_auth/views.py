from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from user_auth.models import UserModel
from user_auth.serializers import RegisterUser, UserProfileSerializer


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


class UserProfileView(GenericAPIView):
    queryset = UserModel
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = UserModel.objects.get(username=self.request.user.username)
        except ObjectDoesNotExist:
            return Response(
                {"message": "User does not exist, try again"},
                status=HTTP_404_NOT_FOUND,
            )
        try:
            user.username = self.request.data["username"]
            user.photo = self.request.FILES["photo"]
            user.description = self.request.data["description"]
            serializer = self.serializer_class(user)
            serializer.is_valid(raise_exception=True)
            user.save()
        except ValueError:
            return Response(
                {"message": "The entered data is incorrect"},
                status=HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.data, status=HTTP_200_OK)
