from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone
from datetime import timedelta

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or not request.user.is_staff:
            return False
            
        if request.method == "POST":
            return False
        
        return True

    def has_object_permission(self, request, view, obj):
        if not request.user.is_staff:
            return False
        
        return True