from rest_framework import permissions
class PublicOfferListPermission(permissions.BasePermission):
    """
    - Erlaubt GET (Liste) für alle, auch nicht-authentifizierte Nutzer.
    - POST ist nur für authentifizierte Nutzer mit user.type == 'business' erlaubt.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  

        if request.method == 'POST':
            return (
                request.user.is_authenticated and 
                getattr(request.user, 'type', None) == 'business'
            )

        return request.user.is_authenticated
    

class AuthenticatedOfferDetailPermission(permissions.BasePermission):
    """
    Nur authentifizierte Nutzer dürfen:
    - GET (Details lesen)
    - PATCH, DELETE (nur, wenn Besitzer)
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated  

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'DELETE']:
            return obj.user == request.user  
        return True  