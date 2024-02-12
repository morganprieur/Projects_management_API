from django.shortcuts import render 
from django.contrib.auth.models import (User) 
from .softdesk.serializers import (UserSerializer) 


class SignupView(CreateAPIView): 
    pass 



class NewClientView(CreateAPIView): 
    
    # Authentication required 
    permission_classes = [IsAdminAuthenticated,]  # IsManagerGroup| 
    serializer_class = ClientSerializer 
    queryset = Client.objects.all() 
