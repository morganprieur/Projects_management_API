
from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from django.contrib.auth.models import User 
from users.models import ( 
    Contributor, UserProfile 
) 


class UserAdmin(BaseUserAdmin): 
    list_display = ( 
        'id', 
        'username', 
        # 'groups_ids', 
        # 'groups_names', 
        'is_staff', 
    ) 

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

# Re-register UserAdmin
admin.site.unregister(User) 
admin.site.register(User, UserAdmin) 


class UserProfileAdmin(admin.ModelAdmin): 
    list_display = ( 
        'pk', 
        # 'user', 
        'age', 
        'can_be_contacted', 
        'data_can_be_shared', 
        'created_time', 
    ) 
admin.site.register(UserProfile, UserProfileAdmin) 


class ContributorAdmin(admin.ModelAdmin): 
    list_display = ( 
        'pk', 
        'user', 
        'project', 
        'created_time', 
    ) 
admin.site.register(Contributor, ContributorAdmin) 


