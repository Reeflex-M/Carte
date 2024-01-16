from django.contrib import admin
from django.urls import path, include
#from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token
from .views.register import register_view as RegisterView
from battle.views import LoginView, RegisterView

urlpatterns = [
    #Admin route
 path('admin/', admin.site.urls),
    #App battle
 path('battle/', include('battle.urls')),
    #register/Login
 path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
 path('login/', LoginView.as_view(), name='login'),
 path('register/', RegisterView.as_view(), name='register')

 # view login / Register
 #path('login/', auth_views.LoginView.as_view(), name='login'),
 #path('register/', RegisterView, name='register')
 
 
]