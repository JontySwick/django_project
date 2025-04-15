from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tasks', TaskListView)

urlpatterns = router.urls + [
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask_list'),
    path('subtasks/<int:id>', SubTaskDetailUpdateDeleteView.as_view(), name='subtask_one'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]