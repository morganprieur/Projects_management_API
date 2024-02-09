
from django.db import models 
from django.contrib.auth.models import User 
from softdesk.models import Project 


class Contributor(models.Model): 

    user = models.ForeignKey( 
        User, 
        on_delete=models.CASCADE, 
        related_name='contributor_user', 
    ) 
    project = models.ForeignKey( 
        Project, 
        on_delete=models.CASCADE, 
        related_name='contributor_project', 
    ) 
    created_time = models.DateTimeField( 
        auto_now_add=True 
    ) 

