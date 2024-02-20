
from django.contrib.auth.models import User 
from softdesk.models import Project 
from users.models import (UserProfile, Contributor) 
from users.serializers import ( 
    UserSerializer, 
    UserPofileSerializer, 
    ContributorSerializer, 
) 
# from django_filters import rest_framework as filters 

from rest_framework import generics, viewsets 
from rest_framework.generics import CreateAPIView, DestroyAPIView 
from django.views.generic.edit import DeleteView 
from rest_framework.parsers import JSONParser 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response 
from rest_framework.views import APIView 
from users.permissions import IsAdminAuthenticated 

# import des fonctions authenticate, login et logout 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required 


class UserViewSet(viewsets.ModelViewSet): 
    """
        API endpoint that allows users to be created, viewed or edited. 
    """ 
    queryset = User.objects.all().order_by('-date_joined') 
    serializer_class = UserSerializer 
    permission_classes = [IsAuthenticated, IsAdminAuthenticated] 


class SignupView(CreateAPIView): 

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
        serializer = UserPofileSerializer(data=data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=201) 
        return Response(serializer.errors, status=400) 


class UserProfileViewSet(viewsets.ModelViewSet): 
    """ 
        The UserProfile's views of the connected User. 
    """ 
    queryset = UserProfile.objects.all() 
    serializer_class = UserPofileSerializer 
    permission_classes = [IsAuthenticated, IsAdminAuthenticated] 
    model = UserProfile 

    def get(self, request): 
        user = request.user 
        profile = UserProfile.objects.get(user=user) 
        serializer = UserPofileSerializer(profile) 
        return Response(serializer.data) 

    def put(self, request): 
        data = JSONParser().parse(request) 
        profile = UserProfile.objects.get(user__username=request.user.username) 
        
        serializer = UserPofileSerializer(profile, data=data, partial=True) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=201) 
        return Response(serializer.errors, status=400) 


class UserProfileView(APIView): 
    """ 
        The UserProfile's views of the connected User. 
    """ 
    serializer_class = UserPofileSerializer 
    permission_classes = [IsAuthenticated] 
    model = UserProfile 

    def get(self, request): 
        user = request.user 
        profile = UserProfile.objects.get(user=user) 
        serializer = UserPofileSerializer(profile) 
        return Response(serializer.data) 


class DeleteUserView(DestroyAPIView): 
    """ Deletes the UserProfile of the designed User. 
        A Signal will delete the user himself 
        after the deletion of the UserProfile. 
    """ 
    queryset = UserProfile.objects.all() 
    serializer_class = UserPofileSerializer 
    permission_classes = [IsAdminAuthenticated, IsAuthenticated] 


class ContributorsListView(APIView): 
    """ Displays a list of the contributors of a given project. 
        Everyon allowed to see them. 
        params: 
            project_id (int): The id of the desired Project. 
    """ 
    # permission_classes = [IsAuthenticated] 

    def get(self, request, project_id, *args, **kwargs): 
        contributors = Contributor.objects.filter(project=project_id) 
        serializer = ContributorSerializer(contributors, many=True) 
        return Response(serializer.data) 


class LogoutView(APIView): 
    """ 
        View to logout the user. 
    """ 
    permission_classes = [IsAuthenticated] 
    def post(self, request): 
        logout(request) 
        return Response({'message': "Logout successful"}) 


# BUG: username + password + name projet obligatoires 
class ContributorViewSet(viewsets.ModelViewSet): 
    """ Set a User to access and contribute to a Project. 
        Only the author of the Project is allowed to add a Contributor. 
        Args: 
            ModelViewSet: Viewset related of a Model, indicated into queryset. .
        Returns: 
            Response: The data or the reason of not serve the data. 
    """ 
    serializer_class = ContributorSerializer 
    permission_classes = [IsAuthenticated] 
    queryset = Contributor.objects.all() 

    def create(self, request): 
        data = request.data 
        # Check if the connected user is the author of the project: 
        connected_user = User.objects.get(username=request.user) 
        project = Project.objects.get(pk=data['project']) 
        if connected_user != project.author: 
            return Response(status=403) 
        serializer = ContributorSerializer(data=data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=200) 
        return Response(serializer.errors, status=400) 

