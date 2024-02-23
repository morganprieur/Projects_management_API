"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path 
from rest_framework import routers 
# JWT 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, 
) 
# drf_spectacular 
from drf_spectacular.views import ( 
    SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView, 
) 

from users import views as users_views 
from softdesk import views as softdesk_views 

router = routers.DefaultRouter() 
# users_views 
router.register(r"users", users_views.UserViewSet, basename='users') 
# router.register(r"contributors", users_views.ContributorViewSet, basename='contributors') 
# router.register(r"profiles", users_views.UserProfileViewSet, basename='profiles') 

urlpatterns = [ 
    # api 
    path('api-auth/', include('rest_framework.urls')), 
    path('', include(router.urls)), 

    # users app 
    # user 
    path('signup/', users_views.SignupView.as_view(), name='signup'), 
    path('profile/', users_views.UserProfileView.as_view(), name='profile'), 
    path('logout/', users_views.LogoutView.as_view(), name='logout'), 
    # contributor 
    path('contributor/', users_views.ContributorView.as_view()), 
    path('contributor/<pk>/', users_views.ContributorView.as_view()), 
    path('contributors/', users_views.ContributorsListView.as_view()), 
    path('project_contributors/<project_id>/', users_views.ProjectContributorsListView.as_view()), 
    path('user_projects/', users_views.ContributionsListView.as_view()), 

    # softdesk app 
    # project 
    path('projects/', softdesk_views.ProjectsListView.as_view()), 
    path('project/', softdesk_views.ProjectView.as_view()), 
    path('project/<pk>/', softdesk_views.ProjectView.as_view()), 
    # issue 
    path('issues/', softdesk_views.IssuesListView.as_view()), 
    path('issue/', softdesk_views.IssueView.as_view()), 
    path('issue/<pk>/', softdesk_views.IssueView.as_view()), 
    path('project_issues/<project_id>/', softdesk_views.IssuesProjectListView.as_view()), 
    path('user_issues/', softdesk_views.IssuesUserListView.as_view()), 
    # comment 
    path('comments/', softdesk_views.CommentListView.as_view(), name='comments'), 
    path('comment/', softdesk_views.CommentView.as_view(), name='comment'), 
    path('comment/<pk>/', softdesk_views.CommentView.as_view(), name='comment'), 
    path('issue_comments/<issue_id>/', softdesk_views.CommentsIssueListView.as_view()), 
    path('user_comments/', softdesk_views.CommentsUserListView.as_view()), 

    # admin routes 
    path('delete_user/<pk>/', users_views.DeleteUserView.as_view(), name='delete_profile'), 
    # Admin interface access 
    path('admin/', admin.site.urls), 

    # JWT login 
    path('jwt/get_token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 

    # Doc: drf_spectacular (dl YAML file) 
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Doc: UI: 
    path('api/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), 

] 
