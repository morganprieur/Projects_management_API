from softdesk.models import (
    UserProfile 
) 
from django.contrib.auth.hashers import make_password 
from django.contrib.auth.models import User, Group 
from django.db.models.signals import post_save 
from django.dispatch import receiver 
from datetime import datetime 


# Quand on crée un Client : 
#   un User est créé, 
#   et le groupe "owner_group" est ajouté à ses groupes 
@receiver(post_save, sender=Client) 
def create_owner_user(sender, instance, created, **kwargs): 
    """ When a Client instance is created: 
            creates a User with name 'cli_' + instance name 
            and assign the new User a 'owner_group'.  
        Args:
            sender (Client): the model sends a signal when an instance is created 
            instance (Client): the just created Client 
            created (bool): the Client instance is created True/False : trigger. If False, the program exits the method.  
    """ 
    # Création d'un User, avec mot de pass hashé 
    if created: 
        new_user = User(username='cli_' + str(instance.name), email='') 
        if len(instance.password) < 20: 
            new_user.password = make_password(instance.password) 
        else: 
            # instance.password is already hashed: 
            new_user.password = instance.password 
        new_user.save() 

        # Get the latest instance of created User: 
        user = User.objects.filter().last() 
        
        if user.username == 'cli_' + str(instance.name): 
            # Adds the group 'owner_group' to the user's instance groups 
            owner_group = Group.objects.get(name='owner_group') 
            user.groups.add(owner_group) 
            
            # Afficher la réussite de la création du User et la liste de ses groupes 
            user_groups = user.groups.values_list('name', flat = True) 
            groups_as_list = list(user_groups) 
            print('User ' + str(user.username) + ' - groupes : ' + str(groups_as_list) + ' successfully saved!') 


# Quand un User est créé et que son nom commence par 'cli_' : 
#   un Client_profile est créé, qui lie le User et le Client. 
@receiver(post_save, sender=User) 
def create_client_profile(sender, instance, created, **kwargs): 
    """ When a User named 'cli_'+ is created, a Client_profile is created in order to bind the User and the Client 
        Args:
            sender (User): the User model, who sends a signal when a new User with name starting with 'cli_' is created.  
            instance (User): the just created User named 'cli_'+. 
            created (bool): determines if the User has been created. If not: the program exits the method. 
    """ 
    if created: 
        # Automatically creates a client_profile on User creation 
        # and links it with the client 
        client = Client.objects.filter().last() 
        user = User.objects.filter(username__startswith='cli_').last() 
        
        if user == instance: 
            Client_profile.objects.create(client_user=instance, client=client) 



# Quand on crée un Bei : 
#   - un User est créé, 
#   - le groupe "bei_group" est ajouté à ses groupes 
@receiver(post_save, sender=Bei) 
def create_bei_user(sender, instance, created, **kwargs): 
    """ When a Bei instance is created: 
        creates a User with name 'bei_' + instance name 
        and assign the new User a 'bei_group'.  
        Args:
            sender (Bei): the model sends a signal when an instance is created 
            instance (Bei): the just created Bei 
            created (bool): the Bei instance is created True/False : trigger. If False, the program exits the method.  
    """ 
    if created: 
        # Création d'un User, avec mot de pass hashé 
        # User.objects.create(username='bei_' + str(instance), email='', password='pass_bei1') 
        new_user = User( 
            username='bei_' + str(instance.serial_number), 
            email='' 
        ) 
        if len(instance.password) < 20: 
            new_user.password = make_password(instance.password) 
        else: 
            # instance.password is already hashed 
            new_user.password = instance.password  
        new_user.save() 
        
        # Get the latest instance of created User 
        user = User.objects.filter().last() 
        
        if user.username == 'bei_' + str(instance): 
            # Adds the group 'bei_group' to the user's instance groups 
            bei_group = Group.objects.get(name='bei_group') 
            user.groups.add(bei_group) 
            
            # Afficher la réussite de la création du User et la liste de ses groupes 
            user_groups = user.groups.values_list('name', flat = True) 
            groups_as_list = list(user_groups) 
            print('User ' + str(user.username) + ' - groupes : ' + str(groups_as_list) + ' successfully saved!') 

        
        if (Bei.objects.last() == str(instance)) and Installation.objects.last().bei == str(instance): 
            last_bei=Bei.objects.last() 
            last_installation = Installation.objects.last() 
            # print(f'last_bei DSIG109 : {last_bei}') 
            # print(f'last_installation DSIG110 : {last_installation}') 

            new_maintenance = Maintenance( 
                bei=last_bei[0], 
                description = 'Installation', 
                maintenance_name = f'Installation {last_bei[0].serial_number}', 
                maintenance_date = last_installation.installation_date 
            ) 
            new_maintenance.save() 
            print(f'new_maintenance DSIG115 : {Maintenance.objects.last()}') 


# Quand un User est créé et que son nom commence par 'bei_' : 
#   un Bei_profile est créé, qui lie le User et le Bei. 
@receiver(post_save, sender=User) 
def create_bei_profile(sender, instance, created, **kwargs): 
    """ When a User with name 'bei_'+ is created: 
            creates a Bei_profile, in order to bind the User and the Client.   
            Args:
                sender (User): the model sends a signal when an instance is created 
                instance (User): the just created User 
                created (bool): the User instance is created True/False: trigger. If False, the program exits the method.  
    """ 
    bei = Bei.objects.filter().last() 
    user = User.objects.filter(username__startswith='bei_').last() 
    
    if created and user == instance: 
        Bei_profile.objects.create(bei_user=instance, bei=bei) 


