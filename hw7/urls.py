from django.urls import path

from . import views

urlpatterns = [
    path("", views.greeting_action, name="index"),
]