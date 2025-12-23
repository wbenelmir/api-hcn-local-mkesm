from rest_framework import permissions
from rest_framework.permissions import BasePermission

def user_in_group(user, group_name: str) -> bool:
    return user and user.is_authenticated and user.groups.filter(name=group_name).exists()

class IsNESDAGroup(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or user_in_group(request.user, "NESDA")

class IsANGEMGroup(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or user_in_group(request.user, "ANGEM")
    
class IsStaffEditorPermission(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
