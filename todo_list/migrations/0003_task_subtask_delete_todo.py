# Generated by Django 5.1.1 on 2024-09-29 16:16

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0002_rename_todoitem_todo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=20)),
                ('color', models.CharField(max_length=20)),
                ('created_at', models.DateField(default=datetime.date.today)),
                ('due_date', models.DateField(default=datetime.date.today)),
                ('checked', models.BooleanField(default=False)),
                ('priority', models.CharField(max_length=20)),
                ('members', models.ManyToManyField(related_name='yourmodel_members', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subtask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=20)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtasks', to='todo_list.task')),
            ],
        ),
        migrations.DeleteModel(
            name='Todo',
        ),
    ]