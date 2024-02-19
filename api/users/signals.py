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
        # print(dir(instance)) 
        new_contrib = Contributor.objects.create( 
            user=instance.author, 
            project=instance 
        )  
        new_contrib.save() 

        # # DEBUG Get the latest instance of created Contrib: 
        # contrib = Contributor.objects.last() 
        # print(f'''Contrib : 
        #     {str(contrib.user.username)} - {str(contrib.project)} 
        #     successfully saved!''') 

