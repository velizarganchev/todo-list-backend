# Generated by Django 5.1.1 on 2024-10-03 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0005_alter_task_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('todo', 'Todo'), ('in_progress', 'In Progress'), ('await_feedback', 'Await feedback'), ('done', 'Done')], default='todo', max_length=20),
        ),
    ]
