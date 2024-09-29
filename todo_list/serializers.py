from rest_framework import serializers
from django.contrib.auth.models import User
from todo_list.models import Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TaskItemSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'category', 'description', 'status',
                  'color', 'priority', 'members', 'created_at', 'due_date', 'checked']
