from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsEmployee(BasePermission):
    """
    Permission for Employees
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_employee)


class IsManager(BasePermission):
    """
    Permission for Employees
    """

    def has_permission(self, request, view):
        return bool(request.user
                    and request.user.is_authenticated
                    and request.user.is_employee
                    and request.user.is_manager
                    )


class IsManagerOrReadOnly(BasePermission):
    """

    """
    def has_permission(self, request, view):
        return bool((request.user
                    and request.user.is_authenticated
                    and request.user.is_employee
                    and request.user.is_manager)
                    or request.method in SAFE_METHODS
                    )
