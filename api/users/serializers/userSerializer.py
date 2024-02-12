
from django.contrib.auth.models import User 
# utils 
from rest_framework import serializers 
import re 
from datetime import datetime, timedelta 
# from django.contrib.auth.hashers import make_password 


class UserSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = User 
        fields = ( 
            'id', 
            'username', 
            'password', 
            'groups', 
        ) 

    def create(self, validated_data): 
        if 'user' in validated_data.keys(): 
            validated_user_data = validated_data['user'] 
            # validated_user_data['password'] = make_password(validated_user_data['password']) 
            return User.objects.create(**validated_user_data) 

