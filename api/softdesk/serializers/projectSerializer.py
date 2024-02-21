

from django.contrib.auth.models import User 
from softdesk.models import Project 
from users.serializers import UserSerializer 
# utils 
from rest_framework import serializers 
# import re 
# from datetime import datetime, timedelta 


class ProjectSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Project 
        fields = ( 
            'id', 
            'author', 
            'name', 
            'description', 
            'type', 
            'created_time', 
        ) 

