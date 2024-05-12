from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReviewCommentPermission(BasePermission):
    """
    Управляет доступом к ресурсам REVIEWS и COMMENTS. Разрешает использовать:
    * безопасные методы - любому пользователю;
    * POST - авторизованному пользователю;
    * остальные методы - администраторам, модераторам или владельцу объекта.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.method == "POST"
            or request.user == obj.author
            or request.user.is_admin
            or request.user.is_moderator
        )


class IsAdmin(BasePermission):
    """Разрешения только для админов"""

    def has_permission(self, request, view):
        return request.user.is_admin


class IsAdminOrReadOnly(BasePermission):
    """Разрешения только для админов или чтения."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )
