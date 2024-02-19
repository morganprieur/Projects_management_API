

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

    # Custom create() 
    def create(self, validated_data): 
        # print(f'validated_data PS41 : {validated_data}') 

        if 'author' in validated_data.keys(): 
            author_data = validated_data.pop('author') 
            # print(f'author_data PS33 : {author_data}') 

            get_author = User.objects.get( 
                username=author_data) 
            # print(f'author PS41 : {get_author}') 

            new_project = Project.objects.create( 
                author=get_author, 
                **validated_data 
            ) 
            return new_project 

