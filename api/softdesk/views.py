from django.shortcuts import render 
from django.contrib.auth.models import User 
from softdesk.models import Project 
from softdesk.serializers import CreateProjectSerializer 
from users.serializers import UserSerializer 
# from users.views import UserViewSet 

from rest_framework import generics, viewsets 
from rest_framework.generics import CreateAPIView 
from rest_framework.parsers import JSONParser 
from rest_framework.response import Response 


class ProjectViewSet(viewsets.ModelViewSet): 
    queryset = Project.objects.all().order_by('-created_time') 
    serializer_class = CreateProjectSerializer 
    model = Project 

    # def create(self, request, *args, **kwargs): 
    #     # print(request) 
    #     # print(dir(request)) 
    #     # user_id = request.user.id 
    #     # print('user id : ', user_id) 
    #     # project_data = request.data['project'] 
    #     data = request.data 
    #     print('data project : ', data) 

    #     # user = request.user.id 
    #     # user_object = User.objects.get(id=request.user.id) 

    #     # user_data = UserSerializer(data=user_object) 
    #     # print('user_data : ', user_data) 

    #     # project_data['author']['id'] = user_id 

    #     # project_data['author'] = {} 
    #     # project_data['author']['id'] = user 
    #     # project_data['author'] = user 

    #     author_req = User.objects.get(id=request.user.id) 
    #     author_data = UserSerializer(author_req) 

    #     data['author'] = author_data 
    #     # data['author'] = {} 
    #     # data['author']['id'] = request.user.id 
    #     # user = User.objects.get(id=request.user.id) 
    #     # data['author']['username'] = user.username 
    #     # data['author']['password'] = user.password 

    #     serializer = ProjectSerializer(data=data) 
    #     print('serializer.initial_data : ', serializer.initial_data) 

    #     if serializer.is_valid(): 
    #         print('serializer.validated_data', serializer.validated_data) 
    #         serializer.save() 
    #         print('serializer.data', serializer.data) 
    #         return Response(serializer.data, status=201) 
    #     return Response(serializer.errors, status=400) 

        # new_project = Project.objects.create( 
        #     name=project_data['name'], 
        #     description=project_data['description'], 
        #     type=project_data['type'], 
        #     # created_time=data['created_time'], 
        # ) 
        # new_project.save() 
        # # serializer = ProjectSerializer(new_project) 
        # return Response(ProjectSerializer.data) 

    # # ne rentre pas dans post : 
    # def post(self, request): 
    #     print('request : ', request) 
    #     data = JSONParser().parse(request) 
    #     print('data views : ', data) 
        
    #     serializer = ProjectSerializer(data=data) 
    #     print('serializer.initial_data : ', serializer.initial_data) 
    #     print('serializer.is_valid', serializer.is_valid()) 
    #     if serializer.is_valid(): 
    #         # serializer.save() 
    #         print('serializer.validated_data1', serializer.validated_data) 
    #         serializer.save( 
    #             type=data['project']['type'], 
    #             name=data['project']['name'], 
    #             description=data['project']['description'] 
    #         )
    #         print('serializer.validated_data2', serializer.validated_data) 
    #         print('serializer.data', serializer.data) 
    #         # print('serializer.initial_data2 : ', serializer.initial_data) 
    #         return Response(serializer.data, status=201) 
    #     return Response(serializer.errors, status=400) 

    # def post(self, request): 
    #     data = JSONParser().parse(request) 
    #     print('data views : ', data) 
        
    #     serializer = ProjectSerializer(data=data) 
    #     if serializer.is_valid(): 
    #         print('valid ok') 
    #         print('valid ? ', serializer) 
    #         serializer.save() 
    #         return Response(serializer.data, status=201) 
    #     return Response(serializer.errors, status=400) 

# class UserList(generics.CreateAPIView):
#     model = Profile
#     serializer_class = ProfileSerializer
#     permission_classes = (IsAuthenticated,) 

# class NewProjectView(CreateAPIView): 
#     model = Project 
#     serializer_class = CreateProjectSerializer 
#     # Authentication required 
#     # permission_classes = [IsAdminAuthenticated,]  # IsManagerGroup| 
#     # queryset = Project.objects.all() 
#     # serializer_class = ProjectSerializer 
#     # parser_classes = [JSONParser] 

#     # def post(self, request): 
#     #     print('request : ', request) 
#     #     data = JSONParser().parse(request) 
#     #     print('data views : ', data) 

#     #     data['author'] = User.objects.get(id=request.user.id) 

#     #     serializer = ProjectSerializer(data=data) 
#     #     print('serializer.initial_data : ', serializer.initial_data) 
#     #     print('serializer.is_valid', serializer.is_valid()) 
#     #     if serializer.is_valid(): 
#     #         # serializer.save() 
#     #         print('serializer.validated_data1', serializer.validated_data) 
#     #         serializer.save( 
#     #             type=data['project']['type'], 
#     #             name=data['project']['name'], 
#     #             description=data['project']['description'] 
#     #         )
#     #         print('serializer.validated_data2', serializer.validated_data) 
#     #         print('serializer.data', serializer.data) 
#     #         # print('serializer.initial_data2 : ', serializer.initial_data) 
#     #         return Response(serializer.data, status=201) 
#     #     return Response(serializer.errors, status=400) 


