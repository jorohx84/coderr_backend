from rest_framework import permissions

class IsProfileOwner(permissions.BasePermission):
    """
    Custom permission to allow only the owner of a profile to update it.
    
    """

    def has_object_permission(self, request, view, obj):
        if request.method == 'PATCH':
            return obj.user == request.user
        return True
