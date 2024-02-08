
from django.db import models 


PROJECT_TYPE = ( 
    ("ALL", "ALL"), 
    ("BACK", "BACK-END"), 
    ("FRONT", "FRONT-END"), 
    ("IOS", "IOS"), 
    ("AND", "ANDROID"), 
) 


class Project(models.Model): 
    author = models.ForeignKey( 
        User, 
        on_delete=models.CASCADE, 
        related_name='project_author' 
    ) 
    name = models.CharField(max_length=100) 
    description = models.TextField() 
    type = models.CharField( 
        max_length=5, 
        choices=PROJECT_TYPE, 
        default=PROJECT_TYPE.ALL 
    ) 
    created_time = models.DateTimeField( 
        auto_now_add=True 
    ) 

""" 
    Seuls les contributeurs d’un projet peuvent accéder à ce dernier. 
        Seuls les contributeurs peuvent accéder aux ressources qui référencent un projet 
            issue 
            comment
    Le contributor est une ressource spécifique, qui lie un utilisateur à un projet.
""" 

