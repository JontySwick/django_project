from django.db import models

possible_statuses = [
    ('new', 'New'),
    ('in_progress', 'In progress'),
    ('pending', 'Pending'),
    ('blocked', 'Blocked'),
    ('done', 'Done'),
]


class Category(models.Model):
    name = models.CharField(max_length=200)


class Task(models.Model):
    title = models.CharField(max_length=256, unique_for_date='created_at')
    description = models.CharField(max_length=512)
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=12, choices=possible_statuses)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField()


class SubTask(models.Model):
    title = models.CharField(max_length=200, unique_for_date='created_at')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=12, choices=possible_statuses)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField()
