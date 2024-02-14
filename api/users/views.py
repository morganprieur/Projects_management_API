
# from django.shortcuts import render 
from django.contrib.auth.models import User  # , Group 
from users.models import UserProfile  # Contributor, 
from users.serializers import ( 
    UserSerializer, 
    UserPofileSerializer, 
) 
# from django_filters import rest_framework as filters 

from rest_framework.permissions import IsAuthenticated 
# from uthdemo.permissions import ( 
#     IsAdminAuthenticated, 
#     IsEditorGroup, 
#     IsRecorderGroup, 
#     IsReaderGroup 
# ) 
from rest_framework import generics, viewsets 
from rest_framework.generics import CreateAPIView 
from rest_framework.parsers import JSONParser 
from rest_framework.response import Response 
from rest_framework.views import APIView 

# from django.views.generic import View 

from django.conf import settings 

# import des fonctions authenticate, login et logout 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required 

from django.db.models import Q 


class UserViewSet(viewsets.ModelViewSet): 
    """
        API endpoint that allows users to be created, viewed or edited. 
    """ 
    queryset = User.objects.all().order_by('-date_joined') 
    serializer_class = UserSerializer 
    permission_classes = [IsAuthenticated] 
    # permission_classes = [permissions.IsAuthenticated] 
    # permission_classes = [IsAdminAuthenticated, ] 

    # def post(self, request):
    #     serializer = UserSerializer(data=request.data) 
    #     if data['age'] < 15: 
    #         return Response(status=status.HTTP_400_BAD_REQUEST)  # *** 
    #     if serializer.is_valid(): 
    #         serializer.save() 
    #         return Response( 
    #             serializer.data, status=status.HTTP_201_CREATED)
    #     return Response( 
    #         serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SignupView(APIView): 
class SignupView(CreateAPIView): 
    # permission_classes = [IsAdminAuthenticated,]  # IsManagerGroup| 
    # serializer_class = UserPofileSerializer 
    # parser_classes = [JSONParser] 

    def post(self, request): 
        """ Sends data for création of a Tech_site instance, 
            binds an Organism, and an Address if needed, 
            and creates an Organism and/or an Address instance 
            if data is given. 
            Args:
                request (dict): the data posted. 
            Returns:
                Response: 
                    201 if the entity/ies has/have been created, 
                    400 with the error if the request has not been completely executed. 
        """ 
        data = JSONParser().parse(request) 
        print('data : ', data) 
        # Save the data to the serializer for validating and saving them into the DB 
        serializer = UserPofileSerializer(data=data) 
        if serializer.is_valid(): 
            print('is_valid yes') 

            serializer.save() 
            return Response(serializer.data, status=201) 
        else: 
            print('is_valid no') 
            return Response(serializer.errors, status=400) 

    # def post(self, request, format=None): 
    #     """ 
    #     """ 
    #     data = JSONParser().parse(request) 
    #     print('data : ', data) 
    #     print('user : ', data['user_profile']['user']) 
    #     print('age : ', data['user_profile']['age']) 
    #     print('can_be_contacted : ', data['user_profile']['can_be_contacted']) 
    #     # Send the data to the serializer for validating 
    #     # and saving them in the DB 
    #     # serializer = InstallationSerializer(data=data_installation) 
    #     serializer = UserPofileSerializer(data=data) 
    #     if serializer.is_valid(): 
    #         print('is_valid') 
    #         serializer.save()
    #         return Response(serializer.data, status=201) 
    #     else: 
    #         print('no') 
    #         return Response(serializer.errors, status=400) 



# class NewClientView(CreateAPIView): 
    
#     # Authentication required 
#     permission_classes = [IsAdminAuthenticated,]  # IsManagerGroup| 
#     serializer_class = ClientSerializer 
#     queryset = Client.objects.all() 



# class BlogPostViewSet(viewsets.ModelViewSet):
#     queryset = BlogPost.objects.all()
#     serializer_class = BlogPostSerializer

