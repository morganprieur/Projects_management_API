
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


# user 
class UserViewSet(viewsets.ModelViewSet): 
    """
        API endpoint that allows users to be created, viewed or edited. 
        Only a superuser is allowed to do this. The users can view and modify 
        their account with the UserProfile methods. 
    """ 
    queryset = User.objects.all().order_by('-date_joined') 
    serializer_class = UserSerializer 
    permission_classes = [IsAuthenticated, IsAdminAuthenticated] 


class SignupView(CreateAPIView): 
    """ Sets a user to interact with the projects. """ 

    def post(self, request): 
        """ Sends data for création of a new User and a new UserProfile instances. 
            Args:
                request (dict): the data posted. 
            Returns:
                Response: 
                    201 if the instance/s has/have been created, 
                    400 with the error if the request has not been completely executed. 
        """ 
        data = request.data 
        # print(data) 
        if data['age'] < 15: 
            return Response('Vous devez être âgé d\'au moins 15 ans.', status=403) 
        serializer = UserPofileSerializer(data=data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=201) 
        return Response(serializer.errors, status=400) 


# user profile 
class UserProfileView(APIView): 
    """ The UserProfile's views of the connected User. """ 
    serializer_class = UserPofileSerializer 
    permission_classes = [IsAuthenticated] 

    def get(self, request): 
        """ Get the connected user's profile. 
            Only the connected user himself can see this 
        """ 
        user = request.user 
        profile = UserProfile.objects.get(user=user) 
        serializer = UserPofileSerializer(profile) 
        return Response(serializer.data) 

    def put(self, request): 
        """ Update the connected user's profile. 
            Only the connected user himself can do this 
        """ 
        data = request.data 
        profile = UserProfile.objects.get(user=request.user) 
        # Check if the updated age is greater than 15: 
        if data['age'] < 15:
            return Response( 
                'Vous devez être âgé d\'au moins 15 ans.', 
                status=403) 
        serializer = UserPofileSerializer(profile, data=data, partial=True) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=201) 
        return Response(serializer.errors, status=400) 

    def delete(self, request): 
        """ Deletes the authenticated user's profile. 
            A Signal will delete the User instance after the UserProfile will 
            be deleted. 
            Only the connected user himself can do this 
        """ 
        user = request.user 
        profile = UserProfile.objects.get(user=user) 
        profile.delete() 
        return Response(status=204) 


class UserProfilesListView(APIView): 
    """ View of all the profiles. 
        Only superusers are allowed to view them. 
    """ 
    permission_classes = [IsAdminAuthenticated] 

    def get(self, request): 
        profiles = UserProfile.objects.all() 
        serializer = UserPofileSerializer(profiles, many=True) 
        return Response(serializer.data, status=200) 


class DeleteUserView(DestroyAPIView): 
    """ Deletes the UserProfile of the designed User. 
        A Signal will delete the user himself after the deletion of the UserProfile. 
        Only a superuser is allowed to do this. 
    """ 
    queryset = UserProfile.objects.all() 
    serializer_class = UserPofileSerializer 
    permission_classes = [IsAdminAuthenticated, IsAuthenticated] 


class LogoutView(APIView): 
    """ 
        View to logout the user. 
    """ 
    permission_classes = [IsAuthenticated] 
    def post(self, request): 
        logout(request) 
        return Response({'message': "Logout successful"}) 


# contributor 
class ContributorView(APIView): 
    """ Actions on the Users who contribute to Projects. 
        All the authenticated users are allowed to view the 
        contributors to a given project. 
        Only the author of a Project is allowed to add or delete another 
        contributor of this project. 
        A user-project binome must be unique. 
        No reason to view or modify a Contributor instance. 
    """ 
    serializer_class = ContributorSerializer 
    permission_classes = [IsAuthenticated] 

    def post(self, request): 
        """ Create a user-project binome. 
            Before that : 
            - check if the connected user is the author of the project, 
            - check if the user-project binome does not already exist. 
        """  
        data = request.data 
        # Check if the connected user is the author of the project: 
        user = request.user 
        project = Project.objects.get(pk=data['project']) 
        if user != project.author: 
            return Response( 
                'Seul l\'auteur du projet peut ajouter un contributeur.', 
                status=403) 
        # Check if the user-project binome does not already exist 
        contributors = Contributor.objects.filter(project=project) 
        already = [] 
        for contrib in contributors: 
            already.append(contrib.user.username) 
        user = User.objects.get(id=data['user']) 
        if user.username in already: 
            return Response( 
                'Cet utilisateur est déjà contributeur sur ce projet.', 
                status=403) 
        serializer = ContributorSerializer(data=data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=200) 
        return Response(serializer.errors, status=400) 

    def delete(self, request, pk): 
        """ Delete a user-project binome. 
            Only the author of the project can do this. 
        """ 
        # Check if the connected user is the author of the project: 
        user = request.user 
        contributor = Contributor.objects.get(id=pk) 
        project = Project.objects.get(id=contributor.project.id) 
        # Check if the user is the project's author. 
        if user != project.author: 
            return Response( 
                'Seul l\'auteur du projet peut supprimer un contributeur.', 
                status=403) 
        else: 
            contributor.delete() 
            return Response(status=204) 


class ContributorsListView(APIView): 
    """ View of all the contributor-project binomes. 
        Only superusers are allowed to view them. 
    """ 
    permission_classes = [IsAdminAuthenticated] 

    def get(self, request): 
        user = request.user 
        if not user.is_superuser: 
            return Response( 
                '''Seul un superutilisateur peut voir tous les contributeurs. 
                Pour voir les contributeurs d\'un projet, ajoutez son ID à la fin de l\'URI''', 
                status=403) 
        else: 
            contributors = Contributor.objects.all() 
            serializer = ContributorSerializer(contributors, many=True) 
            return Response(serializer.data, status=200) 


class ProjectContributorsListView(APIView): 
    """ Displays a list of all the contributors of a given project. 
        Everyone authenticated is allowed to see a project's contributors. 
    """ 
    permission_classes = [IsAuthenticated, IsAdminAuthenticated] 

    def get(self, request, project_id): 
        contributors = Contributor.objects.filter(project=project_id) 
        serializer = ContributorSerializer(contributors, many=True) 
        return Response(serializer.data, status=200) 


class ContributionsListView(APIView): 
    """ Displays a list of the contributions of a user. 
        Only the user is allowed to see his contributions. 
    """ 
    permission_classes = [IsAuthenticated] 

    def get(self, request): 
        contributions = Contributor.objects.filter(user=request.user) 
        serializer = ContributorSerializer(contributions, many=True) 
        return Response(serializer.data, status=200) 


