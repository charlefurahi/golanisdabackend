from rest_framework.permissions import SAFE_METHODS, BasePermission


def _is_admin(user):
    return bool(
        user
        and user.is_authenticated
        and (user.is_staff or user.is_superuser or getattr(user, 'role', None) == 'admin')
    )


class IsAdminOrReadOnly(BasePermission):
    """Anyone can read (list/retrieve); only admins can write."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return _is_admin(request.user)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return _is_admin(request.user)


class IsAdminOnly(BasePermission):
    """Only admins may access this view at all (read or write)."""

    def has_permission(self, request, view):
        return _is_admin(request.user)

    def has_object_permission(self, request, view, obj):
        return _is_admin(request.user)
