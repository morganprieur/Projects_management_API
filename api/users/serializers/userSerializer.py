
from django.contrib.auth.models import User 
# utils 
from rest_framework import serializers 

from users.models import UserProfile 
# utils 
from rest_framework import serializers 
# import re 
# from datetime import datetime, timedelta 
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

    user = UserSerializer() 

    class Meta: 
        model = UserProfile 
        fields = ( 
            'user', 
            'age', 
            'can_be_contacted', 
            'data_can_be_shared', 
            'created_time', 
        ) 

    def create(self, validated_data): 
        print('validated_data UPS41 : ', validated_data) 
        if 'user' in validated_data.keys(): 
            print('user yes') 
            user_data = validated_data.pop('user') 
            user_data['password'] = make_password(user_data['password']) 
            # get_user = User.objects.get(username=user_data['username']) 
            # print('get_user : ', get_user) 
            # if not get_user: 
            new_user = User.objects.create(**user_data) 
            # last_user = User.objects.last() 
            get_user = User.objects.last() 
            print('last_user : ', get_user) 

            return UserProfile.objects.create( 
                user = get_user, 
                **validated_data, 
            ) 


# class UserSerializer(serializers.ModelSerializer): 

#     class Meta: 
#         model = User 
#         fields = ( 
#             'id', 
#             'username', 
#             'password', 
#             'groups', 
#         ) 

#     def create(self, validated_data): 
#         if 'user' in validated_data.keys(): 
#             validated_user_data = validated_data['user'] 
#             validated_user_data['password'] = make_password(validated_user_data['password']) 
#             return User.objects.create(**validated_user_data) 

