from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import TaskListView, SubTaskListCreateView, SubTaskDetailUpdateDeleteView, CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tasks', TaskListView)

urlpatterns = router.urls + [
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask_list'),
    path('subtasks/<int:id>', SubTaskDetailUpdateDeleteView.as_view(), name='subtask_one'),
]