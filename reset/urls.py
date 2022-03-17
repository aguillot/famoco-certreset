from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("devices/", views.DevicesView.as_view(), name="devices"),
    path(
        "reset/<str:org_id>/<str:famoco_id>/", views.ResetView.as_view(), name="reset"
    ),
]
