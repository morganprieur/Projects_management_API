from django.shortcuts import render 
from django.contrib.auth.models import User 
from softdesk.models import Project 
from softdesk.serializers import CreateProjectSerializer 
from users.serializers import UserSerializer 
# from users.views import UserViewSet 

from rest_framework import generics, viewsets 
from rest_framework.generics import CreateAPIView 
from rest_framework.parsers import JSONParser 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response 


class ProjectViewSet(viewsets.ModelViewSet): 
    queryset = Project.objects.all().order_by('-created_time') 
    serializer_class = CreateProjectSerializer 
    permission_classes = [IsAuthenticated] 
    model = Project 


