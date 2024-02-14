
from django.contrib.auth.models import User 
from users.models import UserProfile 

# utils 
from rest_framework import serializers 
from django.contrib.auth.hashers import make_password 
from rest_framework.validators import UniqueValidator 
# import re 
# from datetime import datetime, timedelta 


def minimum_age(value): 
    """ Validator to not create a User instance if the age < 15. 

        Args:
            value (integer): The declared age of the user. 

        Raises:
            serializers.ValidationError: The cause of the error. 
    """ 
    if value < 15:
        raise serializers.ValidationError('Vous devez être âgé d\'au moins 15 ans.') 


class UserSerializer(serializers.ModelSerializer): 
    """ Class to serialize/deserialize a User instance, 
        from the User model. 
    """ 
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
            'user', 
            'age', 
            'can_be_contacted', 
            'data_can_be_shared', 
            'created_time', 
        ) 

    def create(self, validated_data): 
        # print('validated_data UPS41 : ', validated_data) 
        if validated_data['age'] > 15: 
            # print('if > 15') 
            if 'user' in validated_data.keys(): 
                # print('user yes') 
                user_data = validated_data.pop('user') 
                user_data['password'] = make_password(user_data['password']) 

                new_user = User.objects.create(**user_data) 
                get_user = User.objects.last() 
                # print('last_user : ', get_user) 

                return UserProfile.objects.create( 
                    user = get_user, 
                    **validated_data, 
                ) 
        else:  
            # print('else') 
            # print(validated_data['age']) 
            age = minimum_age(validated_data['age']) 
            return False 

