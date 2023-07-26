from rest_framework import permissions

class IsTaskOwner(permissions.BasePermission):
    message = "You don't have permission to edit this task. You are not the owner!"

    def has_object_permission(self, request, view, obj):
        # Allow read-only access for safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the requesting user is the owner of the task object
        return obj.created_by == request.user
