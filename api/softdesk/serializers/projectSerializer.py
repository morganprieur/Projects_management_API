

from django.contrib.auth.models import User 
from softdesk.models import Project 
from users.serializers import UserSerializer, ContributorSerializer 
# utils 
from rest_framework import serializers 
# import re 
# from datetime import datetime, timedelta 


class ProjectSerializer(serializers.ModelSerializer): 
    contributors = ContributorSerializer(many=True) 
    class Meta: 
        model = Project 
        fields = ( 
            'id', 
            'author', 
            'name', 
            'description', 
            'type', 
            'contributors', 
            # 'project_contributors', 
            'created_time', 
        ) 

    # Custom create() 
    def create(self, validated_data): 
        # print(f'validated_data PS41 : {validated_data}') 
        # print(f'validated_data.keys() PS42 : {validated_data.keys()}') 

        if 'author' in validated_data.keys(): 
            author_data = validated_data.pop('author') 
            # print(f'author_data PS33 : {author_data}') 

            get_author = User.objects.get( 
                username=author_data['username']) 
            # print(f'author PS41 : {get_author}') 

            new_project = Project.objects.create( 
                author=get_author, 
                **validated_data 
            ) 
            # print('new project : ', new_project) 
            return new_project 

    # def get(self, data): 
    #     print('data : ', data) 




# class CreateProjectSerializer(serializers.ModelSerializer): 
#     author = UserSerializer() 

#     class Meta: 
#         model = Project 
#         fields = ( 
#             'id', 
#             'author', 
#             'name', 
#             'description', 
#             'type', 
#             'created_time', 
#         ) 
#         extra_kwargs = {'author': {'required': False}} 

#     # Custom create() 
#     def create(self, validated_data): 
#         # print(f'validated_data PS41 : {validated_data}') 
#         # print(f'validated_data.keys() PS42 : {validated_data.keys()}') 

#         if 'author' in validated_data.keys(): 
#             author_data = validated_data.pop('author') 
#             # print(f'author_data PS33 : {author_data}') 

#             get_author = User.objects.get( 
#                 username=author_data['username']) 
#             # print(f'author PS41 : {get_author}') 

#             new_project = Project.objects.create( 
#                 author=get_author, 
#                 **validated_data 
#             ) 
#             # print('new project : ', new_project) 
#             return new_project 

