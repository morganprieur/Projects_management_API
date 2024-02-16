

from django.contrib.auth.models import User 
from softdesk.models import Project 
from users.serializers import UserSerializer, ContributorSerializer 
# utils 
from rest_framework import serializers 
# import re 
# from datetime import datetime, timedelta 


class ProjectSerializer(serializers.ModelSerializer): 
    author = UserSerializer() 

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
        extra_kwargs = {'author': {'required': False}} 

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


class CreateProjectSerializer(serializers.ModelSerializer): 
    # author = UserSerializer() 
    author = serializers.HiddenField( 
        default=serializers.CurrentUserDefault() 
    ) 
    # author = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault() 
    # ) 
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

    # Custom create() 
    def create(self, validated_data): 
        print(f'validated_data PS41 : {validated_data}') 
        print(f'validated_data.keys() PS42 : {validated_data.keys()}') 

        if 'author' in validated_data.keys(): 
            author_data = validated_data.pop('author') 
            print(f'author_data PS49 : {author_data}') 

            # if not User.objects.get(username=author_data): 
            #     new_author = Address.objects.create( 
            #         **author_data 
            #     ) 
            # else: 
            new_author = User.objects.get(username=author_data) 
            print(f'author PS66 : {new_author}') 

            new_project = Project.objects.create( 
                author=new_author, 
                **validated_data 
            ) 
            print('new project : ', new_project) 
            return new_project 

            # self.new_address, created = Address.objects.get_or_create( 
            #     code=address_code, 
            #     **address_data 
            # ) 
        # else: 
        #     new_address = None 

        # if 'author' in validated_data.keys(): 
        #     author_data = validated_data.pop('author') 
        #     # author_data = dict(validated_data.pop('author')) 
        #     print('author_data : ', author_data) 

        #     author = User.objects.get(username=author_data) 

        #     new_project = Project.objects.create( 
        #         author=author, 
        #         **validated_data 
        #     )
        #     return new_project 

        # if 'address' in validated_data.keys(): 
        #     address_data = dict(validated_data.pop('address')) 
        #     # print(f'address_data ITSS88 : {address_data}') 
        #     # address_code = {} 
        #     address_code = address_data.pop('code') 
        #     # print(f'ts_address_code ITSS91 : {address_code}') 
        #     # print(f'ts_address_data ITSS92 : {address_data}') 
        #     """ Traiter l'erreur "unique together" : """ 
        #     last_addresses = Address.objects.filter( 
        #         Q(code=address_code) | Q(**address_data) 
        #     ) 
        #     if not last_addresses: 
        #         new_address = Address.objects.create( 
        #             code=address_code, 
        #             **address_data 
        #         ) 
        #     else: 
        #         new_address = Address.objects.get( 
        #             Q(code=address_code) | Q(**address_data) 
        #         ) 
        #         print(f'same addresses ITSS107 : {last_addresses}') 
        #     # self.new_address, created = Address.objects.get_or_create( 
        #     #     code=address_code, 
        #     #     **address_data 
        #     # ) 
        # else: 
        #     new_address = None 

        # # Check if 'owner' exists or create it 
        # if 'owner' in validated_data.keys(): 
        #     owner_data = dict(validated_data.pop('owner')) 
        #     owner_code = owner_data.pop('code') 

        #     last_owner = Organism.objects.filter( 
        #         Q(code=owner_code) | Q(**owner_data) 
        #     ) 
        #     if not last_owner: 
        #         new_owner = Organism.objects.create( 
        #             code=owner_code, 
        #             **owner_data 
        #         ) 
        #     else: 
        #         new_owner = Organism.objects.get( 
        #             Q(code=owner_code) | Q(**owner_data) 
        #         ) 
        #     # self.new_owner, created = Organism.objects.get_or_create( 
        #     #     address=new_owner_address, 
        #     #     code=owner_code, 
        #     #     **owner_data 
        #     # ) 
        # else: 
        #     new_owner = None 

        # # Check if 'manager' exists or create it 
        # if 'manager' in validated_data.keys(): 
        #     manager_data = dict(validated_data.pop('manager')) 
        #     manager_code = manager_data.pop('code') 

        #     last_manager = Organism.objects.filter( 
        #         Q(code=manager_code) | Q(**manager_data) 
        #     ) 
        #     if not last_manager: 
        #         new_manager = Organism.objects.create( 
        #             code=manager_code, 
        #             **manager_data 
        #         ) 
        #     else: 
        #         new_manager = Organism.objects.get( 
        #             Q(code=manager_code) | Q(**manager_data) 
        #         ) 
        # else: 
        #     new_manager = None 

        # if 'user' in validated_data.keys(): 
        #     user_data = validated_data.pop('user') 
        #     user_code = user_data.pop('code') 

        #     last_users = Organism.objects.filter( 
        #         Q(code=user_code) | Q(**user_data) 
        #     ) 
        #     # for l_u in last_users: 
        #     #     print(f'last_user : {l_u}') 
        #     if not last_users: 
        #         new_user = Organism.objects.create( 
        #             code=user_code, 
        #             **user_data 
        #         ) 
        #     else: 
        #         # new_user = Organism.objects.filter( 
        #         new_user = Organism.objects.get( 
        #             Q(code=user_code) | Q(**user_data)  
        #         ) 
        # else: 
        #     new_user = None 

        # tech_site_code = validated_data.pop('code') 
        # last_tech_sites = Tech_site.objects.filter( 
        #     Q(code=tech_site_code) | Q(**validated_data) 
        # ) 
        # if not last_tech_sites: 
        #     new_tech_site = Tech_site.objects.create( 
        #         address=new_address, 
        #         owner=new_owner, 
        #         manager=new_manager, 
        #         user=new_user, 
        #         # user=new_user[0], 
        #         code=tech_site_code, 
        #         **validated_data 
        #     ) 
        # else: 
        #     new_tech_site = Tech_site.objects.get( 
        #         Q(code=tech_site_code) | Q(**validated_data) 
        #     ) 

        # new_tech_site = self.check_sub_entity(validated_data, Tech_site) 

        # # Return a Tech_site instance 
        # return new_tech_site 
