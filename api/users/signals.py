from users.models import (Contributor) 
from softdesk.models import (Project) 
# from django.contrib.auth.hashers import make_password 
from django.contrib.auth.models import User, Group 
from django.db.models.signals import post_save 
from django.dispatch import receiver 
from datetime import datetime 


# Quand on crée un Project : 
#   un Contributor est créé 
@receiver(post_save, sender=Project) 
def create_contributor(sender, instance, created, **kwargs): 
    """ When a Project instance is created: 
            creates a Contributor.  
        Args:
            sender (Project): the model sends a signal when an instance is created 
            instance (Project): the just created Project 
            created (bool): the Project instance is created True/False : trigger. 
                If False, the program exits the method.  
    """ 
    # Création d'un Contributor. 
    if created: 
        print(dir(instance)) 
        new_contrib = Contributor.objects.create(user=instance.author, project=instance)  
        #  username='cli_' + str(instance.name), email='') 
        # if len(instance.password) < 20: 
        #     new_user.password = make_password(instance.password) 
        # else: 
        #     # instance.password is already hashed: 
        #     new_user.password = instance.password 
        new_contrib.save() 

        # DEBUG Get the latest instance of created Contrib: 
        contrib = Contributor.objects.last() 

        # if user.username == 'cli_' + str(instance.name): 
        #     # Adds the group 'owner_group' to the user's instance groups 
        #     owner_group = Group.objects.get(name='owner_group') 
        #     user.groups.add(owner_group) 
            
        #     # Afficher la réussite de la création du User et la liste de ses groupes 
        #     user_groups = user.groups.values_list('name', flat = True) 
        #     groups_as_list = list(user_groups) 
        #     print('User ' + str(user.username) + ' - groupes : ' + str(groups_as_list) + ' successfully saved!') 
        print('Contrib ' + str(contrib.user.username) + ' successfully saved!') 


# # Quand un User est créé et que son nom commence par 'cli_' : 
# #   un Client_profile est créé, qui lie le User et le Client. 
# @receiver(post_save, sender=User) 
# def create_client_profile(sender, instance, created, **kwargs): 
#     """ When a User named 'cli_'+ is created, a Client_profile is created in order to bind the User and the Client 
#         Args:
#             sender (User): the User model, who sends a signal when a new User with name starting with 'cli_' is created.  
#             instance (User): the just created User named 'cli_'+. 
#             created (bool): determines if the User has been created. If not: the program exits the method. 
#     """ 
#     if created: 
#         # Automatically creates a client_profile on User creation 
#         # and links it with the client 
#         client = Client.objects.filter().last() 
#         user = User.objects.filter(username__startswith='cli_').last() 
        
#         if user == instance: 
#             Client_profile.objects.create(client_user=instance, client=client) 

