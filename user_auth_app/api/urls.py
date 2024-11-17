
from django.urls import path

from user_auth_app.api.views import Auth_View


urlpatterns = [
    path('', Auth_View.as_view()),
]
