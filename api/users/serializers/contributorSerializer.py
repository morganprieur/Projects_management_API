
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

    def create(self, validated_data): 
        # if 'user' in validated_data.keys(): 
        user_data = validated_data.pop('user') 
        print(f'user_data PS32 : {user_data}') 

        get_user = User.objects.get( 
            username=user_data['username']) 
        print(f'get_user PS41 : {get_user}') 

        project_data = validated_data.pop('project') 
        print(f'project_data PS40 : {project_data}') 

        get_project = Project.objects.get( 
            name=project_data['name']) 
        print(f'project PS44 : {get_project}') 

        new_contributor = Contributor.objects.create( 
            user=get_user, 
            project=get_project, 
            **validated_data 
        ) 
        print('user : ', get_user.username, ' projet : ', get_project.name) 
        return new_contributor 

