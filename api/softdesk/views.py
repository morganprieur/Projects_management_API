from django.contrib.auth.models import User 
from django.shortcuts import render 
from softdesk.models import Comment, Issue, Project 
from users.models import Contributor 
from softdesk.serializers import ( 
    CommentSerializer, IssueSerializer, ProjectSerializer) 
from users.serializers import UserSerializer 

from rest_framework import generics, viewsets 
# from rest_framework.generics import CreateAPIView 
from rest_framework.parsers import JSONParser 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response 
from rest_framework.views import APIView 


class GetProjectView(APIView): 
    """ Views a project. 
        Everyone can do this. 
    """ 
    def get(self, request, pk): 
        """ View of a Project instance. 
        """ 
        user = request.user 
        project = Project.objects.get(id=pk) 
        serializer = ProjectSerializer(project) 
        return Response(serializer.data, status=200) 


class ProjectView(APIView): 
    """ Actions on a Project instance. """ 
    permission_classes = [IsAuthenticated] 

    def post(self, request): 
        """ Creates a new Project instance. 
            Only a connected user can do this. 
            A Signal will create the Contributor instance after 
            the Project instance is created. 
        """ 
        user = request.user 
        data = request.data 
        data['author'] = user.pk 
        serializer = ProjectSerializer(data=data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=201) 
        return Response(serializer.errors, status=400) 

    def put(self, request, pk): 
        """ Updates a Project instance. 
            Only the project's author can do this. 
        """ 
        user = request.user 
        data = request.data 
        project = Project.objects.get(id=pk) 
        # Check if the user is the project's author. 
        if user != project.author: 
            return Response('Seul l\'auteur du projet a le droit de le modifier.', 
            status=403) 
        else: 
            data['author'] = user.id 
            data['id'] = pk 
            data['name'] = project.name
            serializer = ProjectSerializer(project, data=data, partial=True) 
            if serializer.is_valid(): 
                serializer.save() 
                return Response(serializer.data, status=201)     
            return Response(serializer.errors, status=400)     

    def delete(self, request, pk): 
        """ Deletes a project instance. 
            Only the project's author is allowed to do that. 
        """ 
        user = request.user 
        # check if the user is the project's author 
        project = Project.objects.get(id=pk) 
        if user != project.author: 
            return Response('Seul l\'auteur du projet peut le supprimer.', 
                status=403) 
        else: 
            project.delete() 
            return Response(status=204) 


class ProjectsListView(APIView): 
    """ Displays a list of all the projects. 
        Everyone authenticated is allowed to see the projects. 
    """ 

    def get(self, request): 
        projects = Project.objects.all() 
        serializer = ProjectSerializer(projects, many=True) 
        return Response(serializer.data, status=200) 


# issue 
class GetIssueView(APIView): 
    """ View an issue. 
    """ 
    def get(self, request, pk): 
        user = User.objects.get(username=request.user) 
        issue = Issue.objects.get(id=pk) 
        serializer = IssueSerializer(issue) 
        return Response(serializer.data, status=200) 


class IssueView(APIView): 
    """ Actions on an Issue instance. 
    """ 
    permission_classes = [IsAuthenticated] 
    
    def post(self, request): 
        """ Creates a new Issue instance. 
            Only the project\'s contributors are allowed 
            to create an issue. 
        """ 
        user = User.objects.get(username=request.user) 
        data = request.data 
        # Check if the user is a contributor of the project. 
        contributors = Contributor.objects.filter(project__id=data['project']) 
        contribs_users = [contrib.user for contrib in contributors] 
        if user not in contribs_users: 
            return Response( 
                'Seul un contributeur du projet peut créer un ticket.', 
                status=403) 
        else: 
            data['author'] = user.pk 
            serializer = IssueSerializer(data=data) 
            if serializer.is_valid(): 
                serializer.save() 
                return Response(serializer.data, status=201) 
            return Response(serializer.errors, status=400) 

    def put(self, request, pk): 
        """ Updates an Issue instance. 
            Only the Issue's author is allowed to do that. 
            He can attribute the issue to another of the issue's 
            contributors. 
        """ 
        user = request.user 
        data = request.data 
        # Check if the connected user is the issue's author 
        issue = Issue.objects.get(id=pk) 
        if user != issue.author: 
            return Response('Seul l\'auteur de l\'issue peut la modifier.', 
                status=403) 
        else: 
            # Check if the new  is in the project.contributors 
            project = Project.objects.get(id=issue.project.id) 
            contributors = Contributor.objects.filter(project=project.id) 
            contribs_ids = [contrib.user.id for contrib in contributors] 
            if data['author'] not in contribs_ids: 
                return Response('Le nouvel auteur doit être déjà contributeur du projet.', 
                status=403) 
            else: 
                data['project'] = issue.project.id 
            serializer = IssueSerializer(issue, data=data, partial=True) 
            if serializer.is_valid(): 
                serializer.save() 
                return Response(serializer.data, status=201) 
            return Response(serializer.errors, status=400) 

    def delete(self, request, pk): 
        """ Deletes an Issue instance. 
            Only the Issue's author is allowed to do that. 
        """ 
        user = User.objects.get(username=request.user) 
        # check if the user is the issue's author 
        issue = Issue.objects.get(id=pk) 
        if user != issue.author: 
            return Response('Seul l\'auteur du ticket peut le supprimer.', 
                status=403) 
        else: 
            issue.delete() 
            return Response(status=204) 


class IssuesListView(APIView): 
    """ Displays a list of all the issues. 
        Everyone authenticated is allowed to see the issues. 
    """ 
    permission_classes = [IsAuthenticated] 

    def get(self, request): 
        issues = Issue.objects.all() 
        serializer = IssueSerializer(issues, many=True) 
        return Response(serializer.data, status=200) 


class IssuesProjectListView(APIView): 
    """ Displays a list of the issues of a given project. 
        Everyone authenticated is allowed to see a project's issues. 
    """ 
    permission_classes = [IsAuthenticated] 

    def get(self, request, project_id): 
        issues = Issue.objects.filter(project=project_id) 
        serializer = IssueSerializer(issues, many=True) 
        return Response(serializer.data, status=200) 


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


# comment 
class GetCommentView(APIView): 
    """ View one comment. 
        Everyone is allowed to vew them. 
    """ 
    def get(self, request, pk): 
        user = request.user 
        comment = Comment.objects.get(uuid=pk) 
        serializer = CommentSerializer(comment) 
        return Response(serializer.data, status=200) 


class CommentView(APIView): 
    """ Actions on one Comment instance. 
    """ 
    permission_classes = [IsAuthenticated] 

    def post(self, request): 
        """ Create a new issue. 
            Only the project's author is allowed to do this. 
        """ 
        user = request.user 
        data = request.data 
        issue = Issue.objects.get(id=data['issue']) 
        # Attribute the author field to the connected user. 
        data['author'] = user.id 
        # Check if the user is the issue's author. 
        if data['author'] != issue.author.id: 
             return Response('Seul l\'auteur de l\'issue peut créer un commentaire.', 
                status=403) 
        else: 
            serializer = CommentSerializer(data=data) 
            if serializer.is_valid(): 
                serializer.save() 
                return Response(serializer.data, status=201) 
            return Response(serializer.errors, status=400) 

    def put(self, request, pk): 
        """ Updates a Comment instance. 
            Only the comment's author is allowed to do that. 
        """ 
        user = request.user 
        data = request.data 
        # Check if the connected user is the issue's author. 
        comment = Comment.objects.get(uuid=pk) 
        if user != comment.author: 
            return Response('Seul l\'auteur du commentaire peut le modifier.', 
                status=403) 
        # Prevent to change the issue 
        data['issue'] = comment.issue.id 
        serializer = CommentSerializer(comment, data=data, partial=True) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=201) 
        return Response(serializer.errors, status=400) 

    def delete(self, request, pk): 
        """ Deletes a comment. 
            Only the author of the comment is allowed to do that. 
        """ 
        user = request.user 
        comment = Comment.objects.get(uuid=pk) 
        # Check if the user is the comment's author. 
        if user != comment.author: 
            return Response('Seul l\'auteur d\'un commentaire peut le supprimer.', 
                status=403) 
        else: 
            comment.delete() 
            return Response(status=204) 


class CommentListView(APIView): 
    """ Viewset of the Comment instances. 
    """ 
    permission_classes = [IsAuthenticated] 

    def get(self, request): 
        comments = Comment.objects.all().order_by('-issue') 
        serializer = CommentSerializer(comments, many=True) 
        return Response(serializer.data, status=200) 


class CommentsIssueListView(APIView): 
    """ View all comments of an issue 
    """ 
    permission_classes = [IsAuthenticated] 

    def get(self, request, issue_id): 
        comments = Comment.objects.filter(issue=issue_id) 
        serializer = CommentSerializer(comments, many=True) 
        return Response(serializer.data, status=200) 


class CommentsUserListView(APIView): 
    """ Displays a list of the comments of the connected user. 
        Only the user is allowed to see all his/her comments in one time. 
    """ 
    permission_classes = [IsAuthenticated] 

    def get(self, request): 
        user = request.user 
        # user = User.objects.get(id=request.user.id) 
        comments = Comment.objects.filter(author=user) 
        serializer = CommentSerializer(comments, many=True) 
        return Response(serializer.data, status=200) 

