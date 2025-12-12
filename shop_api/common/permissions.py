from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone
from datetime import timedelta

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            request.user.is_authenticated
        if request.method == 'GET':
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if not request.user.is_staff:
            return False
        
        return True