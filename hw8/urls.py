from django.urls import path

from . import views


urlpatterns = [
    path("tasks/", views.task_create_or_list, name="task_create_or_list"),
    path("tasks/<int:id>", views.task_one, name="task_one"),
    path("tasks/statistic", views.task_statistic, name="task_one"),
]