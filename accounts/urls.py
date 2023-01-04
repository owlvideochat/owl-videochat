from django.urls import path
from . import views

urlpatterns = [

    #Register
    path('signup/',views.signup,name='signup'),

    #Login
    path('signin/',views.signin,name='signin'),
    
    #Logout
    path('signout/',views.signout,name='signout'),
]