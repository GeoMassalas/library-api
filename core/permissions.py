from rest_framework.permissions import BasePermission


class IsEmployee(BasePermission):
    """
    Permission for Employees
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_employee)
