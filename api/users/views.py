
from django.contrib.auth.models import User 
from users.models import UserProfile  # Contributor, 
from users.serializers import ( 
    UserSerializer, 
    UserPofileSerializer, 
) 
# from django_filters import rest_framework as filters 

from rest_framework import generics, viewsets 
from rest_framework.generics import CreateAPIView 
from rest_framework.parsers import JSONParser 
from rest_framework.permissions import IsAuthenticated 
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


# class SignupView(APIView): 
class SignupView(CreateAPIView): 
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
        # print('data : ', data) 
        # Save the data to the serializer for validating and saving them into the DB. 
        serializer = UserPofileSerializer(data=data) 
        if serializer.is_valid(): 
            # print('is_valid yes') 
            serializer.save() 
            return Response(serializer.data, status=201) 
        else: 
            # print('is_valid no') 
            return Response(serializer.errors, status=400) 

