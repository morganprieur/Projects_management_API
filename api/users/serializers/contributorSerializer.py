
from django.contrib.auth.models import User 
from softdesk.models import Project 
from softdesk.serializers import ProjectSerializer 
from users.models import Contributor, UserProfile 
from users.serializers import UserSerializer 

# utils 
from django.contrib.auth.hashers import make_password 
from rest_framework import serializers 
# import re 
# from datetime import datetime, timedelta 


class ContributorSerializer(serializers.ModelSerializer): 
    """ Class to serialize/deserialize a Contributor instance, 
        from the Contributor model. 
    """ 
    project = ProjectSerializer() 
    user = UserSerializer() 
    class Meta: 
        model = Contributor 
        fields = ( 
            'id', 
            'user', 
            'project', 
            'created_time', 
        ) 


