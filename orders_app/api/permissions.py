from rest_framework.permissions import BasePermission

class OrderPermission(BasePermission):
    """
    Custom permission class for Order views.

    Permissions:
    - POST requests: Only users with type 'customer' can create orders.
    - PATCH requests: Only users with type 'business' can update orders.
    - DELETE requests: Only admin users (is_staff) can delete orders.
    - Other methods: Allowed for any authenticated user.
    
    """

    def has_permission(self, request, view):
        user = request.user

        if request.method == 'POST':
            return user.type == 'customer'

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method == 'PATCH':
            return user.type == 'business'

        if request.method == 'DELETE':
            return user.is_staff

        return True