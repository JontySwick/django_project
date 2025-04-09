from django.urls import path

from . import views
from .views import TaskListView, SubTaskListCreateView, SubTaskDetailUpdateDeleteView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path("tasks/<int:id>", views.task_one, name="task_one"),
    path("tasks/statistic", views.task_statistic, name="task_one"),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask_list'),
    path('subtasks/<int:id>', SubTaskDetailUpdateDeleteView.as_view(), name='subtask_one'),
]