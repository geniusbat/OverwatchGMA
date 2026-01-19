from django.urls import include, path
from rest_framework import routers


from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("delegate_controls/", views.delegate_controlsList.as_view(), name="delegate_controls"),
    path("delegate_controls/<int:pk>", views.delegate_controlsDetail.as_view(), name="delegate_control"),
    path("delegate_errors/", views.delegate_errorsList.as_view(), name="delegate_errors"),
    path("delegate_errors/<int:pk>", views.delegate_errorsDetail.as_view(), name="delegate_error"),
]