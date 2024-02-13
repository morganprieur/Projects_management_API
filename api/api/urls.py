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

# from users import urls 
from users import views as users_views 

from softdesk import views as softdesk_views 

router = routers.DefaultRouter() 
# users_views 
router.register(r"users", users_views.UserViewSet, basename='users') 
# softdesk_views 
router.register(r"projects", softdesk_views.ProjectViewSet, basename='projects') 

urlpatterns = [ 
    # api 
    path('api-auth/', include('rest_framework.urls')), 
    # users app 
    # path('users/', include(router.urls)), 
    path('', include(router.urls)), 
    path('signup/', users_views.SignupView.as_view(), name='signup'), 
    # path('users/signup/', users_views.SignupView.as_view(), name='signup'), 
    # softdesk app 
    # path('new_project/', softdesk_views.NewProjectView.as_view(), name='new_project'), 
    # path('new_project/', softdesk_views.new_project, name='create-ticket'), 
    # admin 
    path('admin/', admin.site.urls), 

]
