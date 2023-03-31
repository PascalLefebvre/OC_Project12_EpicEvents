from rest_framework import permissions


class IsSalesContact(permissions.BasePermission):
    """Permission to check if the authenticated user is the sales contact of \
       the object."""

    message = "You're not allowed because you're not the sales contact of \
               the client."

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return False
        return obj.sales_contact == request.user


class IsClientSupportContact(permissions.BasePermission):
    """Permission to check if the authenticated user is the support \
       contact of the client."""

    message = "You're not allowed because you're not a support contact of \
               the client."

    def is_support_contact(self, request, obj):
        for contract in obj.contract.all():
            for event in contract.event.all():
                if event.support_contact == request.user:
                    return True
        return False

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return self.is_support_contact(request, obj)
        return False
