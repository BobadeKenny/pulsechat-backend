from rest_framework.routers import DefaultRouter

from chats.views import RoomViewSet


router = DefaultRouter()
router.register(r"rooms", RoomViewSet, basename="room")


urlpatterns = [
    
]
urlpatterns += router.urls
