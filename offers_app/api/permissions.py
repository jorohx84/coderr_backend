from rest_framework import permissions

class OfferPermission(permissions.BasePermission):
    """
    Custom permission class for Offer-related actions.

    Rules:
    - POST: Only users with type 'business' are allowed to create offers.
    - PATCH, DELETE: Only the creator (obj.user) of the offer can modify or delete it.
    - Other methods (e.g., GET): Allowed for all authenticated users.

    Notes:
    - Requires authentication to be handled separately, e.g., via IsAuthenticated.
    - Assumes that `request.user` has a `type` attribute (e.g., 'business', 'customer').
    
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.type == 'business'
        
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'DELETE']:
            return obj.user == request.user
        return True

    