from rest_framework.serializers import ModelSerializer

from chats.models import Room, Message


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

    def create(self, validated_data):
        members = validated_data.pop("members", [])
        room = Room.objects.create(**validated_data)
        room.members.set(members)
        room.join(room.owner)
        return room

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"