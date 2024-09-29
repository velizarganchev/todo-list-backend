import datetime
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    members = models.ManyToManyField(User, related_name='yourmodel_members')
    created_at = models.DateField(default=datetime.date.today)
    due_date = models.DateField(default=datetime.date.today)
    checked = models.BooleanField(default=False)
    priority = models.CharField(max_length=20)

    def __str__(self):
        return f'({self.id}) {self.title}'


class Subtask(models.Model):
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    task = models.ForeignKey(
        Task, related_name='subtasks', on_delete=models.CASCADE)

    def __str__(self):
        return f'({self.id}) {self.title}'
