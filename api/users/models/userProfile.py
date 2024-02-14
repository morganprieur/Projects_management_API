
from django.db import models 
from django.contrib.auth.models import User 


class UserProfile(models.Model): 
    user = models.ForeignKey( 
        User, 
        on_delete=models.CASCADE, 
        related_name='profile_user', 
        # blank=True, 
        # null=True, 
    ) 
    age = models.IntegerField( 
        blank=True, 
        null=True, 
    ) 
    can_be_contacted = models.BooleanField(default=False) 
    data_can_be_shared = models.BooleanField(default=False) 
    created_time = models.DateTimeField( 
        auto_now_add=True 
    ) 

