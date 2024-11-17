from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import User_View, UserProfile_View, UserRegister_View, UserLogin_View, UserLogout_View

urlpatterns = [
    path('register/', UserRegister_View.as_view()),
    path('login/', UserLogin_View.as_view()),
    path('logout/', UserLogout_View.as_view()),

    path('contacts/', UserProfile_View.as_view()),
    path('contacts/<int:userprofile_id>/', UserProfile_View.as_view()),

    path('users/', User_View.as_view()),
]
