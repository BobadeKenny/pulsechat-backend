from rest_framework import generics, status
from rest_framework.response import Response


from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers import (
    RegisterUserSerializer,
    LoginUserSerializer,
    LogoutUserSerializer,
    UserSerializer,
)
from users.utils import get_user_tokens


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_tokens = get_user_tokens(user)
        return Response(
            user_tokens,
            status=status.HTTP_201_CREATED,
        )


class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_user_tokens(user)
        return Response(tokens, status=status.HTTP_200_OK)


class LogoutUserView(generics.GenericAPIView):
    serializer_class = LogoutUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
