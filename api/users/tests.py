from django.test import TestCase
from django.urls import reverse 
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

# For permissions 
from django.test import RequestFactory 
from users.permissions import IsAdminAuthenticated 


class ApiTests(TestCase): 
    """ Tests of data contents and formats """ 
    @classmethod 
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


# Only staff can see Users and UserProfiles 
class IsAdminUserTest(TestCase): 
    @classmethod 
    def setUpTestData(self): 
        user = User.objects.create( 
            username='user', 
            is_staff=True, 
            is_superuser=True 
        ) 
        user_profile = UserProfile.objects.create( 
            user=user, age=20) 
        author = User.objects.create( 
            username='author' 
        ) 
        author_profile = UserProfile.objects.create( 
            user=author, age=18) 
        contributor = User.objects.create( 
            username='contributor' 
        ) 
        contributor_profile = UserProfile.objects.create( 
            user=contributor, age=16) 
        project = Project.objects.create( 
            author=author, 
            name='Name project', 
        ) 
        Contributor.objects.create( 
            user=user, 
            project=project, 
        ) 
        Contributor.objects.create( 
            user=contributor, 
            project=project, 
        ) 


    def testOnlyAdminCanGetUsers(self): 
        superuser = User.objects.get(username='user') 
        factory = RequestFactory() 
        # request = factory.delete('/') 
        request = factory.get('users/') 
        request.user = superuser 

        permission_check = IsAdminAuthenticated() 
        permission = permission_check.has_permission( 
            request, None 
        ) 
        self.assertTrue(permission) 


    def testOnlyAdminCanGetProfiles(self): 
        superuser = User.objects.get(username='user') 
        factory = RequestFactory() 

        request = factory.get('profiles/') 
        request.user = superuser 

        permission_check = IsAdminAuthenticated() 
        permission = permission_check.has_permission( 
            request, None 
        ) 
        self.assertTrue(permission) 


    def testOnlyAuthorCanDeleteContributor(self): 
        user = User.objects.get(username='user') 
        author = User.objects.get(username='author') 
        contributor = User.objects.get(username='contributor') 
        projects = Project.objects.all() 
        print(projects) 
        project = Project.objects.get(id=2) 
        print(project) 
        contrib = Contributor.objects.get(user=user) 
        self.assertEquals(contrib.id, 3) 
        self.assertEquals(user.id, 2) 
        self.assertEquals(author.id, 3) 
        self.assertEquals(contributor.id, 4) 
        self.assertEquals(project.id, 2) 
        self.assertEquals(project.author.id, 3) 

        factory = RequestFactory() 
        request = factory.delete('contributors/3/') 
        request.user = user 
        self.assertTrue(request)  # fail --> trouver comment tester ça 
            # la requête doit rentrer dans ContributorViewSet.destroy() 
            # et on doit tester le status http de la Response 

        # c = User() 
        # response = c.get('/contributors/') 
        # self.assertEquals(response.status_code, 200) 
        # # 200 
        # response = c.delete('/contributors/3/')
        # self.assertEquals(response.status_code, 403) 
        # # response.content 


