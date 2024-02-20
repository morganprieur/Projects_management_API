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
router.register(r"contributors", users_views.ContributorViewSet, basename='contributors') 
# router.register(r"profiles", users_views.UserProfileViewSet, basename='profiles') 
# softdesk_views 
router.register(r"projects", softdesk_views.ProjectViewSet, basename='projects') 

urlpatterns = [ 
    # api 
    path('api-auth/', include('rest_framework.urls')), 
    # users app 
    path('', include(router.urls)), 
    path('signup/', users_views.SignupView.as_view(), name='signup'), 
    path('profile/', users_views.GetUserProfileView.as_view({'get':'get'}), name='profile'), 
    path('update_profile/', users_views.UpdateProfileView.as_view({'put':'update'}), name='update_profile'), 
    path('delete_user/<pk>/', users_views.DeleteUserView.as_view(), name='delete_profile'), 
    # path('add_project_contributor/', users_views.AddProjectContributorView.as_view({'post': 'post'}), name='add_contributor'), 
    path('logout/', users_views.LogoutView.as_view(), name='logout'), 
    # softdesk app 

    # admin 
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
