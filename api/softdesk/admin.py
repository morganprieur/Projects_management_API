from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from django.contrib.auth.models import User 
from softdesk.models import ( 
    Comment, 
    # Contributor, 
    Issue, 
    Project, 
    # UserProfile 
) 


# class UserAdmin(BaseUserAdmin): 
#     list_display = ( 
#         'id', 
#         'username', 
#         # 'groups_ids', 
#         # 'groups_names', 
#         'is_staff', 
#     ) 

    # # en-tête de colonnes : 
    # def groups_ids(self, user): 
    #     user_group_ids = user.groups.values_list('id', flat=True)  # QuerySet Object  
    #     group_ids_as_list = list(user_group_ids)  # QuerySet to `list`

    #     text = group_ids_as_list  
    #     return text 
    # groups_ids.short_description = 'Groups ids'

    # def groups_names(self, user): 
    #     user_group_names = user.groups.values_list('name', flat=True)  # QuerySet Object 
    #     group_names_as_list = list(user_group_names)  # QuerySet to `list` 

    #     text = group_names_as_list  
    #     return text 
    # groups_names.short_description = 'Groups names' 

# # Re-register UserAdmin
# admin.site.unregister(User) 
# admin.site.register(User, UserAdmin) 


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

class ProjectAdmin(admin.ModelAdmin): 
    list_display = ( 
        'pk', 
        'author', 
        'name', 
        'description', 
        'type', 
        # 'contributors', 
        'created_time', 
    ) 
    # en-tête de colonnes :  # ne s'affiche pas ? 
    def contribs(self, project): 
        project_contribs_ids = project.contributors.values_list('id', flat=True) 
        contribsList = list(project_contribs_ids) 
        # text = contribsList 
        return contribsList 
    contribs.short_description = 'Contributors ids' 

# class UserAdmin(BaseUserAdmin): 
#     list_display = ('id', 'username', 'groups_ids', 'groups_names', 'is_staff') 

    # en-tête de colonnes : 
    def groups_ids(self, user): 

        user_group_ids = user.groups.values_list('id', flat = True)      # QuerySet Object  
        group_ids_as_list = list(user_group_ids)                        # QuerySet to `list`

        text = group_ids_as_list  
        return text 
    groups_ids.short_description = 'Groups ids'

    def groups_names(self, user): 

        user_group_names = user.groups.values_list('name', flat = True)  # QuerySet Object 
        group_names_as_list = list(user_group_names)                    # QuerySet to `list` 

        text = group_names_as_list  
        return text 
    groups_names.short_description = 'Groups names' 

# # Re-register UserAdmin
# admin.site.unregister(User) 
# admin.site.register(User, UserAdmin) 
admin.site.register(Project, ProjectAdmin) 

class IssueAdmin(admin.ModelAdmin): 
    list_display = ( 
        'pk', 
        'author', 
        'project', 
        'status', 
        'priority', 
        'tag', 
        'created_time', 
    ) 
admin.site.register(Issue, IssueAdmin) 

class CommentAdmin(admin.ModelAdmin): 
    list_display = ( 
        'uuid', 
        'author', 
        'issue', 
        'description', 
        'created_time', 
    ) 
admin.site.register(Comment, CommentAdmin) 

