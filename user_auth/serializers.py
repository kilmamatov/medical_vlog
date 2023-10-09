from rest_framework import serializers

from user_auth.models import UserModel


class RegisterUser(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8)
    password_again = serializers.CharField(min_length=8)
    email = serializers.CharField(max_length=30)

    @staticmethod
    def validate_username(value):
        if UserModel.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь c таким именем уже есть")
        return value

    def validate(self, attrs):
        password = attrs.get("password")
        password_again = attrs.get("password_again")
        if password != password_again:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            "username",
            "photo",
            "email",
            "description",
        )


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=555)


class CreateUserWithEmail(serializers.Serializer):
    email = serializers.CharField(max_length=30)
