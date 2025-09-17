from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework import serializers
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_online",
            "bio",
            "profile_picture",
            "last_seen",
        )
        write_only_fields = ("password",)

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            defaults={
                "first_name": validated_data.get("first_name"),
                "last_name": validated_data.get("last_name"),
                "bio": validated_data.get("bio"),
                "profile_picture": validated_data.get("profile_picture"),
            },
        )
        if created:
            user.set_password(validated_data["password"])
            user.save()
        else:
            raise ValidationError("User with this username or email already exists.")
        return user


class LoginUserSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ("username_or_email", "password")

    def validate(self, attrs):
        username_or_email = attrs.get("username_or_email")
        password = attrs.get("password")

        if not username_or_email or not password:
            raise ValidationError("Both username/email and password are required.")
        return attrs

    def save(self, **kwargs):
        username_or_email = self.validated_data.get("username_or_email")
        password = self.validated_data.get("password")

        try:
            user = User.objects.get(
                Q(username=username_or_email) | Q(email=username_or_email)
            )
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            user = None

        if user is None or not user.check_password(password):
            raise ValidationError("Invalid username/email or password.")

        return user


class LogoutUserSerializer(serializers.Serializer):
    token = serializers.CharField()

    def save(self):
        try:
            RefreshToken(self.validated_data["token"]).blacklist()
        except Exception:
            raise ValidationError("Invalid token or token already blacklisted.")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_online",
            "bio",
            "profile_picture",
            "last_seen",
        )
