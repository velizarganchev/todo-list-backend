from django.contrib import admin

from todo_list.models import Task, Subtask
from user_auth_app.models import UserProfile

# Register your models here.

admin.site.register(Task)
admin.site.register(Subtask)
admin.site.register(UserProfile)
