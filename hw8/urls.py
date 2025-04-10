from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import TaskListView, SubTaskListCreateView, SubTaskDetailUpdateDeleteView, TaskOneView, CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = router.urls + [
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path("tasks/<int:id>", TaskOneView.as_view(), name="task_one"),
    path("tasks/statistic", views.task_statistic, name="task_statistic"),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask_list'),
    path('subtasks/<int:id>', SubTaskDetailUpdateDeleteView.as_view(), name='subtask_one'),
]