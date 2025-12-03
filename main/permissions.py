from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.user == request.user


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read access to everyone,
    but write access only to authenticated users.
    """
    def has_permission(self, request, view):
        # Read permissions for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for authenticated users
        return request.user and request.user.is_authenticated
