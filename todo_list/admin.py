from django.contrib import admin

from todo_list.models import Task, Contact, Subtask

# Register your models here.

admin.site.register(Task)
admin.site.register(Subtask)
admin.site.register(Contact)
