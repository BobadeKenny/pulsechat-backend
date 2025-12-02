from django.shortcuts import render

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from pulsechat.permissions import IsRoomOwner, IsRoomMember
from chats.serializers import RoomSerializer, MessageSerializer
from chats.models import Room, Message


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = [IsAuthenticated, IsRoomOwner]

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAuthenticated(), IsRoomOwner]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        return self.queryset.filter(members=self.request.user)
        
    

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["owner"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
    
class MessageViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsRoomMember]

    def get_queryset(self):
        room_id = self.kwargs.get("room_id")
        return Message.objects.filter(room_id=room_id).order_by("timestamp")
