
from rest_framework import permissions 


class IsAdminAuthenticated(permissions.BasePermission): 
    """ permission class that permits only superusers to request 
        on urls. 
        Args:
            permissions (permissions): class that defines the permissions 
            and their conditions. 
    """ 
    def has_permission(self, request, view): 
        # Access allowed only for superusers. 
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser) 


# def get_users_groups(request): 
#     """ Get the list of the request.user's groups 
#         Args:
#             request (request) 
#         Returns:
#             groups_as_list: list of strings 
#     """ 
#     users_groups = request.user.groups.values_list('name', flat = True) 
#     groups_as_list = list(users_groups) 
#     # print(str(request.user) + ' permissions : ' + str(groups_as_list)) 
#     return groups_as_list 


# class IsOwnerGroup(permissions.BasePermission): 
#     """ permission class that permits only Owners to send requests on urls 
#         Args:
#             permissions (permissions): class that defines the permissions and their conditions 
#     """ 

#     def has_permission(self, request, view): 

#         groups_as_list = get_users_groups(request) 
#         if len(groups_as_list) > 0:  
#             if 'owner_group' in groups_as_list: 
#                 # print('permission group ok') 
#                 return True 
#         else: 
#             print('group pas ok') 
#             return False 


