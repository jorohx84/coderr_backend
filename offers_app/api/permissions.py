from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return request.user.type == 'business'
        return True