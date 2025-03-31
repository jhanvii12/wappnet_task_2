# Generated by Django 5.1.7 on 2025-03-31 07:39

import django.contrib.postgres.fields.ranges
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        ('tasks', '0005_alter_task_dependency'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_type', models.CharField(choices=[('PERSONNEL', 'Personnel'), ('BUDGET', 'Budget'), ('EQUIPMENT', 'Equipment')], max_length=10)),
                ('total_quantity', models.IntegerField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='ResourceAllocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_type', models.CharField(choices=[('PERSONNEL', 'Personnel'), ('BUDGET', 'Budget'), ('EQUIPMENT', 'Equipment')], max_length=10)),
                ('allocated_quantity', models.IntegerField()),
                ('allocation_period', django.contrib.postgres.fields.ranges.DateRangeField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource_allocations', to='projects.project')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource_allocations', to='tasks.task')),
            ],
        ),
    ]
