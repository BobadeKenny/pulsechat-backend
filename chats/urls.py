from rest_framework.routers import DefaultRouter

from chats.views import RoomViewSet, MessageViewset


router = DefaultRouter()
router.register(r"rooms", RoomViewSet, basename="room")
router.register(
    r"rooms/(?P<room_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/messages",
    MessageViewset,
    basename="room-messages",
)


urlpatterns = []
urlpatterns += router.urls
