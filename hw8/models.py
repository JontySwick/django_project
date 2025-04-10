from django.utils import timezone

from django.db import models

from hw8.managers import SoftDeleteManager

POSSIBLE_STATUSES = [
    ('new', 'New'),
    ('in_progress', 'In progress'),
    ('pending', 'Pending'),
    ('blocked', 'Blocked'),
    ('done', 'Done'),
]


class Category(models.Model):
    name = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)

    object = objects = SoftDeleteManager()


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        unique_together = ('name',)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


class Task(models.Model):
    title = models.CharField(max_length=256, unique_for_date='created_at')
    description = models.CharField(max_length=512)
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=12, choices=POSSIBLE_STATUSES)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        unique_together = ('title',)


class SubTask(models.Model):
    title = models.CharField(max_length=200, unique_for_date='created_at')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='sub_tasks')
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=12, choices=POSSIBLE_STATUSES)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'
        unique_together = ('title',)
