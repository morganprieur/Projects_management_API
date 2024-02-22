from django.contrib.auth.models import User 
from django.shortcuts import render 
from softdesk.models import Comment, Issue, Project 
from softdesk.serializers import ( 
    IssueSerializer, ProjectSerializer) 
from users.serializers import UserSerializer 

from rest_framework import generics, viewsets 
# from rest_framework.generics import CreateAPIView 
from rest_framework.parsers import JSONParser 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response 
from rest_framework.views import APIView 

# from django.db.models import Q 


class ProjectViewSet(viewsets.ModelViewSet): 
    """ Viewset of the Project instances. """ 
    queryset = Project.objects.all() 
    serializer_class = ProjectSerializer 
    permission_classes = [IsAuthenticated] 

    def create(self, request): 
        """ Creates a new Project instance. 
            Only a connected user can do this. 
            A Signal will create the Contributor instance after 
            the Project instance is created. 
        """ 
        print(request.data) 
        user = request.user 
        user = User.objects.get(username=user) 
        data = request.data 
        data['author'] = user.pk 
        serializer = ProjectSerializer(data=data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=201) 
        return Response(serializer.errors, status=400) 


class ProjectsListView(APIView): 
    """ Displays a list of the issues of a given project. 
        Everyone authenticated is allowed to see a project's issues. 
    """ 
    permission_classes = [IsAuthenticated] 

    def get(self, request, project_id): 
        issues = Issue.objects.filter(project=project_id) 
        serializer = IssueSerializer(issues, many=True) 
        return Response(serializer.data, status=200) 


class IssueViewSet(viewsets.ModelViewSet): 
    """ Viewset of the Issue instances. 
        Only the project's author is allowed to create an issue. 
        Only the issue's author is allowed to update it. 
        He is allowed to attribute the issue to another project's 
        contributor. 
    """ 
    queryset = Issue.objects.all() 
    serializer_class = IssueSerializer 
    permission_classes = [IsAuthenticated] 

    def create(self, request): 
        """ Creates a new Issue instance. 
            Only the project author is allowed to create an issue. 
        """ 
        user = User.objects.get(username=request.user) 
        print(user) 
        data = request.data 
        print(data) 
        project = Project.objects.get(id=data['project']) 
        print(project) 
        print(project.author) 
        if user != project.author: 
            print('user : ', user, ' project.;author : ', author) 
            return Response( 
                'Seul l\'auteur du projet peut créer un ticket.', 
                status=403) 
        else: 
            data['author'] = user.pk 
            serializer = IssueSerializer(data=data) 
            if serializer.is_valid(): 
                serializer.save() 
                return Response(serializer.data, status=201) 
            return Response(serializer.errors, status=400) 





