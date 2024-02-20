from django.test import TestCase

from users.models import (
    UserProfile, Contributor 
) 
from softdesk.models import ( 
    Comment, Issue, Project  
) 

from django.contrib.auth.models import User  # , Group 

from django.contrib.auth.hashers import make_password 
# from datetime import timedelta 
# import re 


class ApiTests(TestCase): 
    """ Tests of data contents and formats """ 

    @classmethod 
    # def setUpTestData(cls): 
    def setUpTestData(self): 
        # Setup data for tests : 1 user, 1 projet  
        self.user = User.objects.create( 
            username='member_9999', 
            password=make_password('pass_user9999') 
        ) 
        get_user = User.objects.get( 
            username='member_9999' 
        ) 
        self.userProfile = UserProfile.objects.create( 
            user=get_user, 
            age=30, 
            can_be_contacted=True, 
            data_can_be_shared=False 
        ) 
        self.project = Project.objects.create( 
            author=get_user, 
            name='Project test', 
            type='BACK' 
        ) 

    def testUserIsCreated(self): 
        self.user = User.objects.last() 
        self.assertEquals(self.user.id, 1) 


    def testProjectIsCreated(self): 
        self.project = Project.objects.last() 
        self.assertEquals(self.project.id, 1) 

    def testContributorCreatedBySignal(self): 
        self.contrib = Contributor.objects.last() 
        self.assertEquals(self.contrib.id, 1) 


    def testUserProfileDeleted(self): 
        self.assertEquals(UserProfile.objects.last().id, 1) 
        UserProfile.objects.get(id=1).delete() 
        self.assertIsNone(UserProfile.objects.last()) 

    def testUserDeletedBySignal(self): 
        UserProfile.objects.get(id=1).delete() 
        self.assertIsNone(User.objects.last()) 


