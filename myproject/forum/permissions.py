from rest_framework import permissions



# Allows editing only to the author of the object. Others can only read.
class ReadOnly(permissions.BasePermission):  # This is a module for create my own access rights.

    def has_object_permission(self, request, view, obj):  # DRF calls it for each object to check if it can be worked with.
        if request.method in permissions.SAFE_METHODS:  # If this is a "safe" method, we allow everyone
            return True

        return obj.author == request.user  # If the method is not secure (POST, PUT, DELETE), we allow only the author

# Allows deletion only by the author or admin
class AdminAndOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return obj.author == request.user or request.user.is_staff  # "is_staff" - this is a check for admin. Default is True
        return True
