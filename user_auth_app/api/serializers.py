from rest_framework import serializers
from django.contrib.auth.models import User
from todo_list.models import Contact

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name',
                  'email', 'phone_number', 'color']