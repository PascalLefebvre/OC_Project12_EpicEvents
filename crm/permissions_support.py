from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class IsClientSupportContact(permissions.BasePermission):
    """Permission to check if the authenticated user is a support contact."""

    def is_support_contact(self, request, obj):
        for contract in obj.contract.all():
            for event in contract.event.all():
                if event.support_contact == request.user:
                    return True
        self.message = "You're not allowed because you're not a support contact of the client."
        return False

    def has_permission(self, request, view):
        if request.user.team == request.user.SUPPORT:
            if request.method in permissions.SAFE_METHODS:
                return True
        else:
            self.message = (
                "You're not allowed because you're not a support contact."
            )
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return self.is_support_contact(request, obj)
        return False


class IsEventSupportContact(permissions.BasePermission):
    """Permission to check if the authenticated user is the support contact of the event."""

    message = "You're not allowed because you're not the support contact of the event."

    def has_permission(self, request, view):
        if request.user.team == request.user.SUPPORT:
            if request.method not in ["POST"]:
                return True
        else:
            self.message = (
                "You're not allowed because you're not a support contact."
            )
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            self.message = "You're not allowed to delete an event."
            return False
        return obj.support_contact == request.user
