# Generated by Django 5.1.1 on 2024-11-22 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0010_delete_contact_alter_task_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtask',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]