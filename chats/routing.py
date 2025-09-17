from django.urls import path

from chats import consumers


websocket_urlpatterns = [
    path("ws/chats/<uuid:room_id>/", consumers.ChatConsumer.as_asgi()),
]
