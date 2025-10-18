from rest_framework.permissions import BasePermission

class ReviewPermission(BasePermission):
    
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.type == 'customer'
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'DELETE']:
            return obj.reviewer == request.user

        return True  