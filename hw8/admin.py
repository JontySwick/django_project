from django.contrib import admin

from .models import *


class SubTaskInline(admin.StackedInline):
    model = SubTask
    extra = 1


class TaskAdmin(admin.ModelAdmin):
    def short_title(self, obj):
        if len(obj.title) > 13:
            return f'{obj.title[:10]}...'

        return obj.title

    list_display = ('short_title', 'description', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('categories', 'deadline')
    ordering = ('-deadline', 'title')
    list_per_page = 20
    inlines = [SubTaskInline]


class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'description', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('task', 'deadline')
    ordering = ('-deadline', 'title')
    list_per_page = 20

    def action_filter_done(self, request, queryset):
        queryset.filter(status__iexact="Done")

    action_filter_done.short_description = "Filter objects with status is Done"

    actions = [action_filter_done]


class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 20


admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)
admin.site.register(Category, CategoryAdmin)
