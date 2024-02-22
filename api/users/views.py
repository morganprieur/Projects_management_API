
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
        data = JSONParser().parse(request) 
        serializer = UserPofileSerializer(data=data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=201) 
        return Response(serializer.errors, status=400) 


class UserProfileViewSet(viewsets.ModelViewSet): 
    """ The UserProfile's views of the connected User. """ 
    queryset = UserProfile.objects.all() 
    serializer_class = UserPofileSerializer 
    permission_classes = [IsAuthenticated, IsAdminAuthenticated] 
    model = UserProfile 


class UserProfileView(APIView): 
    """ The UserProfile's views of the connected User. """ 
    serializer_class = UserPofileSerializer 
    permission_classes = [IsAuthenticated] 
    model = UserProfile 

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
        data = JSONParser().parse(request) 
        profile = UserProfile.objects.get(user__username=request.user.username) 
        # Check if the updated age is greater than 15: 
        if data['age'] < 15:
            return Response( 
                'Vous devez être âgé d\'au moins 15 ans.', 
                status=400) 

        serializer = UserPofileSerializer(profile, data=data, partial=True) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=201) 
        return Response(serializer.errors, status=400) 

    def delete(self, request): 
        """ Deletes the connected user's profile. 
            A Signal will delete the User instance after the UserProfile will 
            be deleted. 
            Only the connected user himself can do this 
        """ 
        user = request.user 
        profile = UserProfile.objects.get(user__username=user.username) 
        profile.delete() 
        return Response(status=204) 


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


# class ContributorView(APIView): 
class ContributorViewSet(viewsets.ModelViewSet): 
    """ Viewset of the Users who contribute to Projects. 
        Only a superuser is allowed to views all the contributor's records. 
        All the users are allowed to view the contributors to a given project. 
        Only the author of a Project is allowed to add or delete another 
        Contributor to this project. 
        A user-project" binome must be unique. 
    """ 
    serializer_class = ContributorSerializer 
    permission_classes = [IsAuthenticated] 
    queryset = Contributor.objects.all() 

    def list(self, request): 
        """ Get all the contributors and projects. 
            Only a superuser is allowed to view this. 
        """ 
        connected_user = request.user 
        if not connected_user.is_superuser: 
            return Response( 
                'Seul un superutilisateur peut voir tous les contributeurs. \
                Pour voir les contributeurs d\'un projet, ajoutez son ID à la fin de l\'URI', 
                status=403) 


    def create(self, request): 
        """ Create a user-project binome. Before that : 
            - check if the connected user is the author of the project, 
            - check if the user-project binome does not already exist. 
        """  
        data = request.data 
        # Check if the connected user is the author of the project: 
        connected_user = User.objects.get(username=request.user) 
        project = Project.objects.get(pk=data['project']) 
        if connected_user != project.author: 
            print('project id : ', project.id, 'user id : ', connected_user.id) 
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


    def destroy(self, request, pk): 
        """ Delete a user-project binome. 
            Only the author of the project can do this. 
        """ 
        # Check if the connected user is the author of the project: 
        connected_user = User.objects.get(username=request.user) 
        contributor = Contributor.objects.get(pk=pk) 
        project = Project.objects.get(pk=contributor.project.id) 
        # print('user : ', connected_user, ' project.author : ', project.author) 
        serializer = ContributorSerializer(contributor) 
        if connected_user != project.author: 
            # print('project author : ', project.author, 'user id : ', connected_user.id) 
            return Response( 
                'Seul l\'auteur du projet peut supprimer un contributeur.', 
                status=403) 
        else: 
            serializer.delete() 
            return Response(serializer.data, status=204) 


class ContributorsListView(APIView): 
    """ Displays a list of the contributors of a given project. 
        Everyone authenticated is allowed to see a project's contributors. 
    """ 
    permission_classes = [IsAuthenticated] 

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


