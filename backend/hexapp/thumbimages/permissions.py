from rest_framework import permissions
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.permissions import SAFE_METHODS

class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return False


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class CanSee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.has_perm('thumbimage.hide_image') or request.user.is_superuser:
            return True
        return False


class ExpiredObjectSuperuserOnly(permissions.BasePermission):

    message = "This object is expired."

    def object_expired(self, obj):
        second = int(obj.expiry_time)
        expired_on = timezone.make_aware(datetime.now() - timedelta(seconds=second))
        return obj.created < expired_on

    def has_object_permission(self, request, view, obj):

        if self.object_expired(obj) and not request.user.is_superuser:
            return False
        else:
            return True