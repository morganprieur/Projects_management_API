
from users.models import (UserProfile) 
from users.serializers import UserSerializer 
from django.contrib.auth.models import User 
from users.models import UserProfile 
# utils 
from rest_framework import serializers 
import re 
from datetime import datetime, timedelta 
from django.contrib.auth.hashers import make_password 


class UserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = User 
        fields = ( 
            'id', 
            'username', 
            'password', 
            'groups', 
        ) 


class UserPofileSerializer(serializers.ModelSerializer): 

    # user = UserSerializer() 

    class Meta: 
        model = UserProfile 
        fields = ( 
            # 'user', 
            'age', 
            'can_be_contacted', 
            'data_can_be_shared', 
            'created_time', 
        ) 

    def create(self, validated_data): 
        print('validated_data UPS41 : ', validated_data) 
        # if 'user_profile' in validated_data.keys(): 
        #     print('yes') 
            # user_data = validated_data['user_profile'].pop('user') 
            # user_data['password'] = make_password(user_data['password']) 
            # get_user = User.objects.filter(username=user_data['username']) 
            # print('get_user : ', get_user) 
            # if not get_user: 
            #     new_user = User.objects.create( 
            #         user_data) 
            #     # last_user = User.objects.last() 
            #     get_user = User.objects.last() 
            #     print('last_user : ', get_user) 

        return UserProfile.objects.create( 
            # user = get_user, 
            **validated_data 
        ) 

# ======== # 

        # address_data = validated_data['site'].pop('address') 
        # # print(f'address_data DS189 : {address_data}') 
        # new_address = Address.objects.create(**address_data) 
        # # print(f'new_address DS191 : {new_address}') 

        # # Then we create the Site and set the Site.address FK 
        # site_data = validated_data.pop('site') 
        # # print(f'site_data DS195 : {site_data}') 
        # new_site = Site.objects.create( 
        #     address=Address.objects.last(), 
        #     **site_data 
        # )
        # # print(f'new_site DS202 : {new_site}') 

        # client_data = validated_data['bei'].pop('client') 
        # # print(f'client_data DS205 : {client_data}') 

        # # And we create the Bei and set the Bei.client FK 
        # bei_data = validated_data.pop('bei') 
        # # print(f'bei_data DS209 : {bei_data}') 
        # new_bei = Bei.objects.create( 
        #     client=Client.objects.get( 
        #         name=client_data['name'] 
        #     ), 
        #     **bei_data 
        # ) 
        # # print(f'new_bei DS221 : {new_bei}') 

        # # print(f'validated_data DS238 : {validated_data}') 
        # new_installation = Installation.objects.create( 
        #     bei=Bei.objects.last(), 
        #     site=Site.objects.last(), 
        #     **validated_data 
        # ) 

        # # Return a Site instance 
        # return new_installation 

# ======== # 

