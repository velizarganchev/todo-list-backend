from rest_framework import serializers
from django.contrib.auth.models import User
from todo_list.models import Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TaskItemSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'category', 'description', 'status',
                  'color', 'priority', 'members', 'created_at', 'due_date', 'checked']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['members'] = UserSerializer(
            instance.members, many=True).data
        return representation
