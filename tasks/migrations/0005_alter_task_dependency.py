# Generated by Django 5.1.7 on 2025-03-28 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_task_dependency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='dependency',
            field=models.ManyToManyField(blank=True, related_name='dependent_tasks', to='tasks.task'),
        ),
    ]
