from rest_framework import permissions

from accounts.models import sales_group


class IsClientSalesContact(permissions.BasePermission):
    """Permission to check if the authenticated user is a sales contact."""

    message = "You're not allowed because you're not the sales contact of the client."

    def has_permission(self, request, view):
        if sales_group in request.user.groups.all():
            return True
        self.message = "You're not allowed because you're not a sales contact."
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            self.message = "You're not allowed to delete a client."
            return False
        return obj.sales_contact == request.user


class IsEventSalesContact(permissions.BasePermission):
    """Permission to check if the authenticated user is the sales contact of the client for whom the event is organized."""

    message = "You're not allowed because you're not the sales contact of the event client."

    def has_permission(self, request, view):
        if sales_group in request.user.groups.all():
            return True
        self.message = "You're not allowed because you're not a sales contact."
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            self.message = "You're not allowed to delete an event."
            return False
        return obj.contract.sales_contact == request.user
