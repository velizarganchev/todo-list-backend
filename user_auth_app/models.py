from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userprofile")
    phone_number = models.CharField(
        max_length=40, blank=True, null=True, default='')
    color = models.CharField(max_length=40, blank=True, default='green')

    def __str__(self):
        return f'{self.user.username}'
