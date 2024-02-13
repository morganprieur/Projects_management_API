

from django.contrib.auth.models import User 
from softdesk.models import Project 
from users.serializers import UserSerializer 
# utils 
from rest_framework import serializers 
# import re 
# from datetime import datetime, timedelta 


# class ProjectSerializer(serializers.Serializer): 
class ProjectSerializer(serializers.ModelSerializer): 
    author = UserSerializer() 
    class Meta: 
        model = Project 
        fields = ( 
            'pk', 
            'author', 
            'name', 
            'description', 
            'type', 
            'created_time', 
        ) 
    # extra_kwargs = {'name': {'required': False}} 

    # def create(self, validated_data): 
    #     print('validated_data : ', validated_data) 
    #     # if 'author' in validated_data.keys(): 
    #     #     author_data = validated_data['author'].pop('author') 
    #     #     get_user = User.objects.filter( 
    #     #         username=author_data['username']) 
    #     # new_project = Project.objects.create( 
    #     #     # author = get_user, 
    #     #     **validated_data, 
    #     # ) 
    #     return Project.objects.create(**validated_data,) 

