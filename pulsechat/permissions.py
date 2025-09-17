from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from chats.models import Room





class IsRoomOwner(BasePermission):
    message = "Unauthorized"

    def has_permission(self, request, view):
        room_id = view.kwargs.get("room_id")
        user_is_owner = Room.objects.filter(owner=request.user, id=room_id).exists()

        return user_is_owner
    
class IsRoomMember(BasePermission):
    message = "Unauthorized"
    
    def has_permission(self, request, view):
        room_id = view.kwargs.get("room_id")
        user_is_member = Room.objects.filter(id=room_id, members=request.user).exists()
        
        return user_is_member
