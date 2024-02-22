
from django.contrib.auth.models import User 
from softdesk.models import Issue 
from users.serializers import UserSerializer 
# utils 
from rest_framework import serializers 
# import re 
# from datetime import datetime, timedelta 


class Issues(object): 
    def __init__(self, status, priority, tag): 
        self.status = status 
        self.priority = priority 
        self.tag = tag 

ISSUE_STATUS = ( 
    ("TODO", "TO DO"), 
    ("IP", "IN PROGRESS"), 
    ("FINISHED", "FINISHED"), 
) 
ISSUE_PRIORITY = ( 
    ("LOW", "LOW"), 
    ("MEDIUM", "MEDIUM"), 
    ("HIGH", "HIGH"), 
) 
ISSUE_TAG = ( 
    ("BUG", "BUG"), 
    ("FEATURE", "FEATURE"), 
    ("TASK", "TASK"), 
) 


class IssueSerializer(serializers.ModelSerializer): 
    status = serializers.ChoiceField( 
        choices=ISSUE_STATUS, 
        required=False, 
    ) 
    priority = serializers.ChoiceField( 
        choices = ISSUE_PRIORITY, 
        required=False, 
    ) 
    tag = serializers.ChoiceField( 
        choices = ISSUE_TAG) 
    class Meta: 
        model = Issue 
        fields = ( 
            'id', 
            'author', 
            'project', 
            'status', 
            'priority', 
            'tag', 
            'created_time', 
        ) 

    # def create(self, validated_data): 
    #     print(validated_data) 
    #     # if fields == None


# ======== 
# from rest_framework import serializers 
  
# class Geeks(object): 
#     def __init__(self, choices, multiplechoices): 
#         self.choices = choices 
#         self.multiplechoices = multiplechoices 
  
# # create a tuple 
# GEEKS_CHOICES =(  
#     ("1", "One"),  
#     ("2", "Two"),  
#     ("3", "Three"),  
#     ("4", "Four"),  
#     ("5", "Five"),  
# ) 
  
# # create a serializer 
# class GeeksSerializer(serializers.Serializer): 
#     # initialize fields 
#     choices = serializers.ChoiceField( 
#                         choices = GEEKS_CHOICES) 
#     multiplechoices = serializers.MultipleChoiceField( 
#                         choices = GEEKS_CHOICES) 
# ======== 

