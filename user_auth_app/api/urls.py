
from django.urls import path

from user_auth_app.api.views import Auth_View


urlpatterns = [
    path('api/auth/', Auth_View.as_view()),
    # path('api/auth/delete/', Auth_View.as_view()),
]
