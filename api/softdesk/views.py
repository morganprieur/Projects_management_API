from django.contrib.auth.models import User 
from django.shortcuts import render 
from softdesk.models import Comment, Issue, Project 
from users.models import Contributor 
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


class ProjectsViewSet(viewsets.ModelViewSet): 
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


class IssuesProjectListView(APIView): 
    """ Displays a list of the issues of a given project. 
        Everyone authenticated is allowed to see a project's issues. 
    """ 
    permission_classes = [IsAuthenticated] 

    def get(self, request, project_id): 
        issues = Issue.objects.filter(project=project_id) 
        serializer = IssueSerializer(issues, many=True) 
        return Response(serializer.data, status=200) 


class IssuesViewSet(viewsets.ModelViewSet): 
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
        data = request.data 
        project = Project.objects.get(id=data['project']) 
        if user != project.author: 
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


class IssueView(APIView): 
    """ Update and delte an Issue instance. 
    """ 
    def put(self, request, pk): 
        """ Updates an Issue instance. 
            Only the Issue's author is allowed to do that. 
            He can attribute the issue to another of the issue's 
            contributors. 
        """ 
        user = request.user 
        data = request.data 
        print(data) 
        # Check if the connected user is the issue's author 
        issue = Issue.objects.get(id=pk) 
        if user != issue.author: 
            return Response('Seul l\'auteur de l\'issue peut la modifier.', 
                status=403) 
        else: 
            # Check if the data['author'] is in the projrct.contributors 
            project = Project.objects.get(id=issue.project.id) 
            contributors = Contributor.objects.filter(project=project.id) 
            contribs_ids = [contrib.user.id for contrib in contributors] 
            if data['author'] not in contribs_ids: 
                return Response('Le nouvel auteur doit être déjà contributeur du projet.', 
                status=403) 
            serializer = IssueSerializer(issue, data=data, partial=True) 
            if serializer.is_valid(): 
                serializer.save() 
                return Response(serializer.data, status=201) 

    def delete(self, request, pk): 
        """ Deletes an Issue instance. 
            Only the Issue's author is allowed to do that. 
        """ 
        user = User.objects.get(username=request.user) 
        # check if the user is the issue's author 
        issue = Issue.objects.get(id=pk) 
        if user != issue.author: 
            return Response('Seul l\'auteur de l\'issue peut la supprimer.', 
                status=403) 
        else: 
            issue.delete() 
            return Response(status=204) 


class IssuesUserListView(APIView): 
    """ Displays a list of the issues of the connected user. 
        Only the user is allowed to see all his/her issues in one time. 
    """ 
    permission_classes = [IsAuthenticated] 

    def get(self, request): 
        user = User.objects.get(id=request.user.id) 
        issues = Issue.objects.filter(author=user) 
        serializer = IssueSerializer(issues, many=True) 
        return Response(serializer.data, status=200) 



