from django.contrib import admin

from .models import *


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('categories', 'deadline')
    ordering = ('-deadline', 'title')
    list_per_page = 20

class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'description', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('task', 'deadline')
    ordering = ('-deadline', 'title')
    list_per_page = 20


class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 20


admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)
admin.site.register(Category, CategoryAdmin)
