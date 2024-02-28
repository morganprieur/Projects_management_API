
from rest_framework import permissions 
from users.models import Contributor 
from softdesk.models import Project 

class IsAdminAuthenticated(permissions.BasePermission): 
    """ permission class that permits only superusers to request 
        on urls. 
        Args:
            permissions (permissions): class that defines the permissions 
            and their conditions. 
    """ 
    def has_permission(self, request, view): 
        # Access allowed only for superusers. 
        return bool( 
            request.user and 
            request.user.is_authenticated and 
            request.user.is_superuser) 

