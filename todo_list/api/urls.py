from django.contrib import admin
from django.urls import path, include

from todo_list.api.views import AllTasks_View, SingleTask_View, AllSubtasks_View, Subtask_View, All_Contacts_View, Contact_View

urlpatterns = [
    path('all-contacts/', All_Contacts_View.as_view()),
    path('contact/<int:pk>/', Contact_View.as_view()),
    path('all-tasks/', AllTasks_View.as_view()),
    # path('single-task/', SingleTask_View.as_view()),
    path('single-task/<int:pk>/', SingleTask_View.as_view()),
    path('subtask/', AllSubtasks_View.as_view()),
    path('subtask/<int:pk>/', Subtask_View.as_view()),
    # path('subtask/create/<int:task_id>/', Subtask_View.as_view()),
]
