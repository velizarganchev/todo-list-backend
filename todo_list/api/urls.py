from django.contrib import admin
from django.urls import path, include

from todo_list.api.views import Task_View, Subtask_View

urlpatterns = [
    path('tasks/', Task_View.as_view()),
    path('tasks/<int:task_id>/', Task_View.as_view()),
    path('subtask/', Subtask_View.as_view()),
    path('subtask/<int:subtask_id>/', Subtask_View.as_view()),
]
