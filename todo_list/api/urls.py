from django.contrib import admin
from django.urls import path, include

from todo_list.api.views import Task_View, Subtask_View

urlpatterns = [
    path('tasks/', Task_View.as_view(), name='task-list'),
    path('tasks/<int:task_id>/', Task_View.as_view(), name='task-detail'),
    path('subtask/', Subtask_View.as_view(), name='subtask-list'),
    path('subtask/<int:subtask_id>/',
         Subtask_View.as_view(), name='subtask-detail'),
]
