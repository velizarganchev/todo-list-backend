from rest_framework import serializers
from todo_list.models import Subtask, Task
from user_auth_app.models import UserProfile
from user_auth_app.api.serializers import UserProfileSerializer


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'title', 'status']


class TaskItemSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(), many=True)
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

        member_ids = [member.id for member in members_data]

        for member_id in member_ids:
            if not UserProfile.objects.filter(id=member_id).exists():
                raise serializers.ValidationError(
                    f"UserProfile with ID {member_id} does not exist."
                )

        task = Task.objects.create(**validated_data)

        members = UserProfile.objects.filter(id__in=member_ids)
        task.members.set(members)

        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)

        return task

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['members'] = UserProfileSerializer(
            instance.members.all(), many=True).data
        return representation
