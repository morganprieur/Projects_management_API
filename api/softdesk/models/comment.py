
from django.db import models 
from django.contrib.auth.models import User 
from softdesk.models import Issue 


class Issue(models.Model): 

    uuid = models.UUIDField( 
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False 
    ) 
    author = models.ForeignKey( 
        User, 
        on_delete=models.CASCADE, 
        related_name='comment_author' 
    ) 
    issue = models.ForeignKey( 
        Issue, 
        on_delete=models.CASCADE, 
        related_name='comment_issue' 
    ) 
    description = models.CharField( 
        max_length=255, 
    ) 
    created_time = models.DateTimeField( 
        auto_now_add=True 
    ) 

