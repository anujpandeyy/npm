from . import views
from django.urls import path 

urlpatterns = [

path("login/" , views.loginView),
path("signup/",views.signupView),
path("loginsubmit/",views.loginForm),
path("signupsubmit/",views.signup),
path("logout/",views.Logout)

]