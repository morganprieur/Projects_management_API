
from django.contrib.auth.models import User 
from users.models import (Contributor, UserProfile) 

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


class ContributorSerializer(serializers.ModelSerializer): 
    """ Class to serialize/deserialize a Contributor instance, 
        from the Contributor model. 
    """ 
    class Meta: 
        model = Contributor 
        fields = ( 
            'id', 
            'user', 
            'project', 
            'created_time', 
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

    def create(self, instance, validated_data): 
        # print('create instance UPS67 : ', instance) 
        # print('create validated_data UPS68 : ', validated_data) 
        if 'age' in validated_data.keys(): 
            if validated_data['age'] > 15: 
                # print('if age > 15') 
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
        else: 
            profile = profile.update( 
                **validated_data, 
            ) 
            profile.save() 
            print('profile : ', profile) 
            return profile 


        

    # def update(self, validated_data): 
    #     print('update validated_data UPS84 : ', validated_data) 
    #     # updated_profile = {} 
    #     # updated_profile['can_be_contacted'] = validated_data['can_be_contacted'] 
    #     # updated_profile['data_can_be_shared'] = validated_data['data_can_be_shared'] 
    #     # return UserProfile.objects.update( 
    #     #     **updated_profile, 
    #     # ) 


