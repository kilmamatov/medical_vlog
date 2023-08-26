from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from user_auth.models import UserModel
from user_auth.serializers import RegisterUser


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
        user.save()
        return Response({"message": "You have successfully registered"})
