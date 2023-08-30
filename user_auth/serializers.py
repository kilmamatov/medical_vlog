from rest_framework import serializers

from user_auth.models import UserModel


class RegisterUser(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8)
    password_again = serializers.CharField(min_length=8)

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
            "description",
        )


class UserAddPhoto(serializers.Serializer):
    photo = serializers.ImageField()

    class Meta:
        model = UserModel

    def create(self, validated_data):
        user = self.context["request"].user
        user.photo = validated_data["photo"]
        user.save(update_fields=["photo"])
        return user
