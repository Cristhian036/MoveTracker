from django.contrib import admin
from django.urls import path,include
from user import views as user_view
from django.contrib.auth import views as auth

from .router import router
from rest_framework.authtoken import views

urlpatterns = [

    path('admin/', admin.site.urls),

    ######### api path ##########################

    path('api/',include(router.urls)),
    path('api-token-auth/',views.obtain_auth_token,name='api-tokn-auth'),

    #####user related path##########################
    path('',include('user.urls')),
    path('login/',user_view.Login,name='login'),
    path('logout/',auth.LogoutView.as_view(template_name='user/index.html'),name='logout'),
    path('register/',user_view.register,name='register'),

    #####parking related path##########################
    path('parking/',include('parking.urls')),

]
