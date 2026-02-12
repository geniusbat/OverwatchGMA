from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.dashboard),
    path("delegates/", views.delegates, name="delegates"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("master/", views.master, name="master"),
]