import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chats.models import Room


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_id = f"chat_{self.room_id}"
        self.room = Room.objects.get(id=self.room_id)

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

    def room_message(self, event):
        self.send(text_data=json.dumps(event))
