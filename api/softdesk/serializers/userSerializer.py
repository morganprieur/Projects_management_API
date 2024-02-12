
from softdesk.models import ( 
    Comment, Contributor, Issue, Project, UserProfile 
) 
from django.contrib.auth.models import User 
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

    def create(self, validated_data): 
        if 'user' in validated_data.keys(): 
            validated_user_data = validated_data['user'] 
            validated_user_data['password'] = make_password(validated_user_data['password']) 
            return User.objects.create(**validated_user_data) 


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
        validated_data['password'] = make_password(validated_data['password']) 
        return Client.objects.create(**validated_data) 

class AddressSerializer(serializers.ModelSerializer): 

    city = serializers.CharField(max_length=45) 
    zipcode = serializers.CharField(max_length=10) 
    street = serializers.CharField(max_length=45) 
    street_number = serializers.IntegerField() 
    suplement = serializers.CharField( 
        required=False, 
        max_length=45 
    ) 
    lat = serializers.FloatField() 
    lng = serializers.FloatField() 

    class Meta: 
        model = Address 
        fields = (
            'city', 'zipcode', 'street', 'street_number', 
            'suplement', 'lat', 'lng' 
        ) 

class SiteSerializer(serializers.ModelSerializer): 

    name = serializers.CharField(max_length=45) 
    address = AddressSerializer() 

    class Meta: 
        model = Site 
        fields = (
            'name', 
            'address' 
        ) 
    
    # # # Custom create()
    # def create(self, validated_data): 
    #     print(f'validated_data DS85 : {validated_data}') 
    #     # First we create 'address' data for the Address 
    #     address_data = validated_data.pop('address')
    #     address = Address.objects.create(**address_data)

    #     # Now we create the Site and set the Site.address FK 
    #     # site_data = validated_data.pop('site') 
    #     new_site = Site.objects.create(address=address, **validated_data) 
    #     print(f'new_site DS93 : {new_site}') 

    #     # Return a Site instance
    #     return new_site 


class BeiSerializer(serializers.ModelSerializer): 

    serial_number = serializers.CharField(max_length=45) 
    fuel_capacity = serializers.CharField(max_length=45) 
    # client = ClientSerializer()  # name=required=False ??? 
    client = ClientSerializer() 
    password = serializers.CharField(max_length=150) 

    class Meta: 
        model = Bei 
        fields = ( 
            'serial_number', 
            'fuel_capacity', 
            'client', 
            'password' 
        ) 
    
    

class Bei_profileSerializer(serializers.ModelSerializer): 

    bei_user = UserSerializer()  
    bei = BeiSerializer() 

    class Meta: 
        model = Bei_profile 
        fields = ( 
            'bei_user', 
            'bei' 
        ) 

class NewBeiSerializer(serializers.ModelSerializer): 

    serial_number = serializers.CharField(max_length=45) 
    fuel_capacity = serializers.CharField(max_length=45) 
    client = ClientSerializer() 
    password = serializers.CharField(max_length=150) 

    class Meta: 
        model = Bei 
        fields = ( 
            'serial_number', 
            'fuel_capacity', 
            'client', 
            'password' 
        ) 

class InstallationSerializer(serializers.ModelSerializer): 
    
    site = SiteSerializer() 
    bei = BeiSerializer() 
    installation_date = serializers.DateTimeField() 

    class Meta: 
        model = Installation 
        # depth = 1 
        fields = ( 
            'site', 
            'bei', 
            'installation_date' 
        ) 
    
    # Custom create()
    def create(self, validated_data): 
        # print(f'validated_data DS185 : {validated_data}') 
        # print(f'Address.objects.last() DS186 : {Address.objects.last()}') 

        address_data = validated_data['site'].pop('address') 
        # print(f'address_data DS189 : {address_data}') 
        new_address = Address.objects.create(**address_data) 
        # print(f'new_address DS191 : {new_address}') 

        # Then we create the Site and set the Site.address FK 
        site_data = validated_data.pop('site') 
        # print(f'site_data DS195 : {site_data}') 
        new_site = Site.objects.create( 
            address=Address.objects.last(), 
            **site_data 
        )
        # print(f'new_site DS202 : {new_site}') 

        client_data = validated_data['bei'].pop('client') 
        # print(f'client_data DS205 : {client_data}') 

        # And we create the Bei and set the Bei.client FK 
        bei_data = validated_data.pop('bei') 
        # print(f'bei_data DS209 : {bei_data}') 
        new_bei = Bei.objects.create( 
            client=Client.objects.get( 
                name=client_data['name'] 
            ), 
            **bei_data 
        ) 
        # print(f'new_bei DS221 : {new_bei}') 

        # print(f'validated_data DS238 : {validated_data}') 
        new_installation = Installation.objects.create( 
            bei=Bei.objects.last(), 
            site=Site.objects.last(), 
            **validated_data 
        ) 

        # Return a Site instance 
        return new_installation 


