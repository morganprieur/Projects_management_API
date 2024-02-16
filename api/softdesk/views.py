from django.shortcuts import render 
from django.contrib.auth.models import User 
from softdesk.models import Project 
from softdesk.serializers import ProjectSerializer 
from users.serializers import UserSerializer, ContributorSerializer 
# from users.views import UserViewSet 

from rest_framework import generics, viewsets 
from rest_framework.generics import CreateAPIView 
from rest_framework.parsers import JSONParser 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response 
from rest_framework.views import APIView 


class ProjectViewSet(viewsets.ModelViewSet): 
    queryset = Project.objects.all() 
    serializer_class = ProjectSerializer 
    permission_classes = [IsAuthenticated] 
    model = Project 


class CreateProjectView(APIView): 
    queryset = Project.objects.all() 
    serializer_class = ProjectSerializer 
    # serializer_class = CreateProjectSerializer 
    permission_classes = [IsAuthenticated] 
    model = Project 

    def post(self, request): 
        data = JSONParser().parse(request) 
        print('data : ', data) 
        user = request.user 
        user_data = User.objects.get(id=user.id) 
        # data['author'] = dict(User.objects.get(pk=user.id)) 
        # print('data : ', data) 
        data['author'] = {} 
        data['author']['id'] = user_data.id 
        data['author']['username'] = user_data.username 
        data['author']['password'] = user_data.password 
        # print(data) 
        serializer = ProjectSerializer(data=data) 
        print('serializer initial data : ', serializer.initial_data) 
        if serializer.is_valid(): 
            print('serializer.validated_data : ', serializer.validated_data) 
            serializer.save() 
            print('serializer data : ', serializer.data) 
            return Response(serializer.data, status=200) 
        return Response(serializer.errors, status=400) 




