"""
URL configuration for todo_list_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

from todo_list.views import Auth_View, AllTasks_View, SingleTask_View, Subtask_View

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', Auth_View.as_view()),
    path('auth/delete/', Auth_View.as_view()),
    path('all-tasks/', AllTasks_View.as_view()),
    path('single-task/', SingleTask_View.as_view()),
    path('single-task/<int:task_id>/', SingleTask_View.as_view()),
    path('subtask/<int:subtask_id>/', Subtask_View.as_view()),
    path('subtask/create/<int:task_id>/', Subtask_View.as_view()),
]
