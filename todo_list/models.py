import datetime
from django.db import models
from django.contrib.auth.models import User
from user_auth_app.models import UserProfile


class Task(models.Model):
    CATEGORY_CHOICES = [
        ('user_story', 'User Story'),
        ('technical_task', 'Technical Task'),
    ]

    STATUS_CHOICES = [
        ('todo', 'Todo'),
        ('in_progress', 'In Progress'),
        ('await_feedback', 'Await feedback'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=80)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default='user_story')
    description = models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='todo')
    color = models.CharField(max_length=20)
    members = models.ManyToManyField(
        UserProfile, related_name='tasks_as_member')
    created_at = models.DateField(auto_now_add=True)
    due_date = models.DateField(default=datetime.date.today)
    checked = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default='medium')

    def __str__(self):
        return f'({self.id}) {self.title}'

    # def save(self, *args, **kwargs):
    #     for member in self.members.all():
    #         if not isinstance(member, UserProfile):
    #             raise ValueError(
    #                 "Each member must have a valid user profile.")
    #     super().save(*args, **kwargs)


class Subtask(models.Model):
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    task = models.ForeignKey(
        Task, related_name='subtasks', on_delete=models.CASCADE)

    def __str__(self):
        return f'({self.id}) {self.title}'
