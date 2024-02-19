from django.contrib.auth.models import User 
from django.shortcuts import render 
from softdesk.models import Project 
from softdesk.serializers import ProjectSerializer 
from users.serializers import UserSerializer 

from rest_framework import generics, viewsets 
# from rest_framework.generics import CreateAPIView 
from rest_framework.parsers import JSONParser 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response 
# from rest_framework.views import APIView 

# from django.db.models import Q 


class ProjectViewSet(viewsets.ModelViewSet): 
    queryset = Project.objects.all() 
    serializer_class = ProjectSerializer 
    permission_classes = [IsAuthenticated] 
    # model = Project 

    def create(self, request): 
        user = request.user 
        user_object = User.objects.get(username=user) 
        # print(user_object) 
        data = request.data 
        data['author'] = user_object.pk 
        # print(data) 
        serializer = ProjectSerializer(data=data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=200) 
        return Response(serializer.errors, status=400) 

