from rest_framework.permissions import BasePermission, SAFE_METHODS


# Разрешения для пользователей
class IsAdmin(BasePermission):
    # CREATE, LIST
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # можно было написать request.method =='GET
            return True
        return request.user.is_authenticated and request.user.is_staff

    # RETRIEVE,UPDATE,DELETE
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        obj = [IsAuthor]
        print(obj)
        return request.user.is_authenticated and (request.user == obj.author or request.user.is_staff)
