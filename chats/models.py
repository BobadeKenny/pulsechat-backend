from django.db import models
import uuid

from users.models import User


# Create your models here.
class Room(models.Model):
    id = models.UUIDField(
        primary_key=True, editable=False, unique=True, default=uuid.uuid4
    )
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_rooms"
    )
    members = models.ManyToManyField(User, related_name="rooms", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def join(self, user):
        self.members.add(user)
        self.save()

    def leave(self, user):
        self.members.remove(user)
        self.save()


class Message(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    timestamp = models.DateTimeField(auto_now_add=True)
