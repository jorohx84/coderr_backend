from rest_framework.permissions import BasePermission

class ReviewPermission(BasePermission):
    """

    Custom permission for Review model:
    
    - POST requests:
      Only users with type 'customer' are allowed to create reviews.
      
    - PATCH and DELETE requests:
      Only the original reviewer (creator of the review) is allowed to update or delete the review.
      
    - Other requests (e.g., GET):
      Are allowed for any authenticated user.
      
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.type == 'customer'
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'DELETE']:
            return obj.reviewer == request.user

        return True  