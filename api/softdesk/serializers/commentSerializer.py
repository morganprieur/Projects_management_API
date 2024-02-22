
from django.contrib.auth.models import User 
from softdesk.models import Comment, Issue 
from users.serializers import UserSerializer 
# utils 
from rest_framework import serializers 
# import re 
# from datetime import datetime, timedelta 


class CommentSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Comment 
        fields = ( 
            'uuid', 
            'author', 
            'issue', 
            'description', 
            'created_time', 
        ) 



