from rest_framework import serializers
from django.contrib.auth.models import User
from todo_list.models import Subtask, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'title', 'status']


class TaskItemSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True)
    subtasks = SubtaskSerializer(many=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'category', 'description', 'status',
            'color', 'priority', 'members', 'created_at', 'due_date',
            'checked', 'subtasks'
        ]

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        members_data = validated_data.pop('members', [])

        task = Task.objects.create(**validated_data)
        task.members.set(members_data)

        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)

        return task

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['members'] = UserSerializer(
            instance.members.all(), many=True).data
        return representation
