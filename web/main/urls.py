from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.dashboard),
    path("index/", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("master/", views.master, name="master"),
]