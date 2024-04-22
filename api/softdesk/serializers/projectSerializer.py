

from django.contrib.auth.models import User 
from softdesk.models import Project 
from users.serializers import UserSerializer 
# utils 
from rest_framework import serializers 


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

