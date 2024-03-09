from django.urls import path
from . import views, metrics

urlpatterns = [
    path("", views.index, name="index"),
    path("metrics", metrics.metrics, name="metrics"),
]
