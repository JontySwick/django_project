# Generated by Django 5.1.7 on 2025-04-03 20:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, unique_for_date='created_at')),
                ('description', models.CharField(max_length=512)),
                ('status', models.CharField(choices=[('new', 'New'), ('in_progress', 'In progress'), ('pending', 'Pending'), ('blocked', 'Blocked'), ('done', 'Done')], max_length=12)),
                ('deadline', models.DateTimeField()),
                ('created_at', models.DateTimeField()),
                ('categories', models.ManyToManyField(to='hw8.category')),
            ],
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique_for_date='created_at')),
                ('description', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('new', 'New'), ('in_progress', 'In progress'), ('pending', 'Pending'), ('blocked', 'Blocked'), ('done', 'Done')], max_length=12)),
                ('deadline', models.DateTimeField()),
                ('created_at', models.DateTimeField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hw8.task')),
            ],
        ),
    ]
