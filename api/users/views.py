
from django.contrib.auth.models import User 
from users.models import (UserProfile, Contributor) 
from users.serializers import ( 
    UserSerializer, 
    UserPofileSerializer, 
    ContributorSerializer, 
) 
# from django_filters import rest_framework as filters 

from rest_framework import generics, viewsets 
from rest_framework.generics import CreateAPIView 
from rest_framework.parsers import JSONParser 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response 
from rest_framework.views import APIView 

# from django.views.generic import View 

from django.conf import settings 

# import des fonctions authenticate, login et logout 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required 

from django.db.models import Q 


class UserViewSet(viewsets.ModelViewSet): 
    """
        API endpoint that allows users to be created, viewed or edited. 
    """ 
    queryset = User.objects.all().order_by('-date_joined') 
    serializer_class = UserSerializer 
    permission_classes = [IsAuthenticated] 
    # permission_classes = [permissions.IsAuthenticated] 
    # permission_classes = [IsAdminAuthenticated, ] 


# class SignupView(APIView): 
class SignupView(CreateAPIView): 
    # serializer_class = UserPofileSerializer 
    # parser_classes = [JSONParser] 

    def post(self, request): 
        """ Sends data for création of a Tech_site instance, 
            binds an Organism, and an Address if needed, 
            and creates an Organism and/or an Address instance 
            if data is given. 
            Args:
                request (dict): the data posted. 
            Returns:
                Response: 
                    201 if the entity/ies has/have been created, 
                    400 with the error if the request has not been completely executed. 
        """ 
        data = JSONParser().parse(request) 
        # print('data : ', data) 
        # Save the data to the serializer for validating and saving them into the DB. 
        serializer = UserPofileSerializer(data=data) 
        if serializer.is_valid(): 
            # print('is_valid yes') 
            serializer.save() 
            return Response(serializer.data, status=201) 
        else: 
            # print('is_valid no') 
            return Response(serializer.errors, status=400) 


class GetUserProfileView(viewsets.ModelViewSet): 
    serializer_class = UserPofileSerializer 
    permission_classes = [IsAuthenticated] 
    model = UserProfile 

    def get(self, request): 
        user = request.user 
        # print('user : ', user) 
        profile = UserProfile.objects.get(user=user) 
        # print('profile : ', profile) 
        serializer = UserPofileSerializer(profile) 
        return Response(serializer.data) 


class UpdateProfileView(viewsets.ModelViewSet): 
    serializer_class = UserPofileSerializer 
    permission_classes = [IsAuthenticated] 
    queryset = UserProfile.objects.get(user__username='root') 

    def update(self, request): 
        # print('request user : ', request.user) 
        data = JSONParser().parse(request) 
        profile = UserProfile.objects.get(user__username=request.user.username) 
        # print('data : ', data) 
        
        serializer = UserPofileSerializer(profile, data=data, partial=True) 
        # print('serializer initial : ', serializer.initial_data) 
        if serializer.is_valid(): 
            # print('valid') 
            # print('serializer validated : ', serializer.validated_data) 
            serializer.save() 
            return Response(serializer.data, status=201) 
        return Response(serializer.errors, status=400) 


class LogoutView(APIView): 

    def post(self, request): 
        print('request : ', request)
        print('request user : ', request.user)
        logout(request) 
        return Response({'message': "Logout successful"}) 


class ContributorViewSet(viewsets.ModelViewSet): 
    serializer_class = ContributorSerializer 
    permission_classes = [IsAuthenticated] 
    queryset = Contributor.objects.all() 


class AddProjectContributorView(viewsets.ModelViewSet): 
    serializer_class = ContributorSerializer 
    permission_classes = [IsAuthenticated] 
    # quesryset = Contributor.objects.all() 

    def post(self, request): 
        data = JSONParser().parse(request) 
        print(data) 
        serializer = ContributorSerializer(data=data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=200) 
        return Response(serializer.errors, status=400) 


