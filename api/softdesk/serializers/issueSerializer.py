
from django.contrib.auth.models import User 
from softdesk.models import Issue 
from users.serializers import UserSerializer 
# utils 
from rest_framework import serializers 


class Issues(object): 
    def __init__(self, status, priority, tag): 
        self.status = status 
        self.priority = priority 
        self.tag = tag 

ISSUE_STATUS = ( 
    ("TODO", "TO DO"), 
    ("WIP", "IN PROGRESS"), 
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
    """ The issues have default values: 
        status = "todo" and priority = 'low'. 
    """ 
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

