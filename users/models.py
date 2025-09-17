from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True, editable=False, unique=True, default=uuid.uuid4
    )
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    is_online = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return (
            f"{self.first_name} {self.last_name}"
            if self.first_name and self.last_name
            else self.username
        )

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return (
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
        )
