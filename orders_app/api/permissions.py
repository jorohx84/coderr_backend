from rest_framework.permissions import BasePermission, SAFE_METHODS

class OrderPermission(BasePermission):
    """
    - POST: Nur 'customer'
    - PATCH: Nur 'business'
    - DELETE: Nur Admins (is_staff)
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if request.method == 'POST':
            return user.type == 'customer'
        
        if request.method == 'PATCH':
            return user.type == 'business'
        
        if request.method == 'DELETE':
            return user.is_staff

        return True