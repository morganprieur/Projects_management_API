from django.shortcuts import render 
from django.contrib.auth.models import User 
from softdesk.models import Project 
from softdesk.serializers import ProjectSerializer 
from users.models import Contributor 
from users.serializers import UserSerializer, ContributorSerializer 
# from users.views import UserViewSet 

from rest_framework import generics, viewsets 
from rest_framework.generics import CreateAPIView 
from rest_framework.parsers import JSONParser 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response 
from rest_framework.views import APIView 

from django.db.models import Q 


# class ProjectViewSet(viewsets.ModelViewSet): 
class ProjectView(APIView): 
    # queryset = Project.objects.all() 
    # serializer_class = ProjectSerializer 
    permission_classes = [IsAuthenticated] 
    # model = Project 

    def get(self, request): 
        projects = [] 
        contributors = [] 

        projects_only = Project.objects.all() 
        for proj in projects_only: 
            # song = Song.objects.get(id='<the-song-id>')
            # users_that_like_this_song = song.users_that_like_me.all()
            # contribs = proj.contributors.all() 
            # users_that_like_this_song.filter(name='Jon')
            contribs = Contributor.objects.filter( 
                project=proj 
            ) 
            print('contribs : ', contribs) 
            print(proj.id) 
            print(proj.author) 
            print(proj.name) 
            print(proj.description) 
            print(proj.type)  
            # for contrib in contribs: 
            for contrib in contribs: 
                print(contrib.id)  
                print(contrib.project)  
                print(contrib.user) 
                # print('dir(proj) : ', dir(proj)) 
                # contrib_serializer = ContributorSerializer( 
                #     contrib, context={ 
                #         'id': contrib.id, 
                #         'project': contrib.project, 
                #         'user': contrib.user, 
                #     }
                # ) 
                # contributors.append(contrib_serializer.data) 
                contributors.append(contrib) 
                # print('contributors : ', contributors) 
            serializer = ProjectSerializer( 
                proj, context={ 
                    'id': proj.id, 
                    'author': proj.author, 
                    'name': proj.name, 
                    'description': proj.description, 
                    'type': proj.type, 
                    'contributors': ContributorSerializer( 
                        contributors, context={ 
                            'id': contrib.id, 
                            'project': contrib.project, 
                            'user': contrib.user, 
                        }, 
                    ) , 
                    # { 
                    #     'id': contrib.id, 
                    #     'project': contrib.project, 
                    #     'user': contrib.user, 
                    # }, 
                    'created_time': proj.created_time, 
                }, 
                # contrib_serializer, context={ 
                #     'id': contrib.id, 
                #     'project': contrib.project, 
                #     'user': contrib.user, 
                # }
            ) 
            # print('serializer.initial_data : ', serializer.initial_data)
            print('serializer.data : ', serializer.data)
            projects.append(serializer.data) 
        return Response(projects) 

    # def get(self, request): 

    #     locations = [] 

    #     # Get the entities 
    #     user = User.objects.get(id=request.user.id) 
    #     client_user = Client_profile.objects.get( 
    #         client_user=user 
    #     ) 
    #     beiList = Bei.objects.filter( 
    #         client=client_user.client 
    #     ) 

    #     # Loop into the registered beis 
    #     for registered_bei in beiList: 
    #         install = Installation.objects.get(bei=registered_bei) 
    #         # Send the installation for the current bei and client 
    #         serializer = LocationSerializer( 
    #             install, context={ 
    #                 'id': install.id, 
    #                 'bei': install.bei.serial_number, 
    #                 'client': install.bei.client.id 
    #             } 
    #         ) 
    #         locations.append(serializer.data) 

    #     return Response(locations) 

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
            return Response(serializer.data, status=201) 
        return Response(serializer.errors, status=400) 

