
from django.contrib.auth.models import User 
from users.models import UserProfile 

# utils 
from django.contrib.auth.hashers import make_password 
from rest_framework import serializers 
from rest_framework.validators import UniqueValidator 


class UserSerializer(serializers.ModelSerializer): 
    """ Class to serialize/deserialize a User instance, 
        from the User model. 
    """ 
    username = serializers.CharField() 
    class Meta: 
        model = User 
        fields = ( 
            'id', 
            'username', 
            'password', 
            'groups', 
        ) 


class UserPofileSerializer(serializers.ModelSerializer): 
    """ Class to serialize/deserialize a UserProfile instance, 
        from the UserProfile model. 

        Returns:
            UserProlife: A UserProfile or some UserProfile instances. 
    """ 
    user = UserSerializer() 

    class Meta: 
        model = UserProfile 
        fields = ( 
            'id', 
            'user', 
            'age', 
            'can_be_contacted', 
            'data_can_be_shared', 
            'created_time', 
        ) 


    def create(self, validated_data): 
        if 'user' in validated_data.keys(): 
            user_data = validated_data.pop('user') 
            user_data['password'] = make_password(user_data['password']) 

            new_user = User.objects.create(**user_data) 
            get_user = User.objects.last() 

            return UserProfile.objects.create( 
                user = get_user, 
                **validated_data, 
            ) 
        

