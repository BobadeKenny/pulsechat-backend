import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chats.models import Room, Message
from users.models import User


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        self.room = None
        self.user_id = None
        self.room_id = None
        self.room_group_id = None
        super().__init__(*args, **kwargs)

    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_id = f"chat_{self.room_id}"
        self.room = Room.objects.get(id=self.room_id)
        self.user_id = self.scope["user_id"]
        if not self.user_id:
            self.close()
            return
        try:
            self.user = User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            self.close()
            return

        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_id, self.channel_name
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_id, self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_id,
            {
                "type": "room_message",
                "message": message,
            },
        )
        Message.objects.create(content=message, user=self.user, room=self.room)

    def room_message(self, event):
        self.send(text_data=json.dumps(event))
