# Generated by Django 5.1.1 on 2024-11-07 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0008_alter_task_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='color',
            field=models.CharField(default='green', max_length=40),
        ),
    ]
