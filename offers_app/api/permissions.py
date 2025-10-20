from rest_framework import permissions

class OfferPermission(permissions.BasePermission):
    """
    - GET, HEAD, OPTIONS: für alle erlaubt (auch nicht-authentifizierte Nutzer)
    - POST: nur authentifizierte Nutzer mit `type='business'`
    - PATCH, DELETE: nur Besitzer des Objekts (authentifiziert)
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            return request.user.is_authenticated and request.user.type == 'business'

        return request.user.is_authenticated  

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'DELETE']:
            return obj.user == request.user
        return True