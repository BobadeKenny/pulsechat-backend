from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from users.views import RegisterUserView, LoginUserView, LogoutUserView, UserDetailView

urlpatterns = [
    path("auth/register/", RegisterUserView.as_view(), name="register"),
    path("auth/login/", LoginUserView.as_view(), name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/logout/", LogoutUserView.as_view(), name="logout"),
    path("auth/user/", UserDetailView.as_view(), name="user-detail"),
]
