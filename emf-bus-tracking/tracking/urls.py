from django.urls import path
from . import views, metrics

urlpatterns = [
    path("", views.index, name="index"),
    path("webhooks/kosmos", views.kosmos_webhook, name="kosmos_webhook"),
    path("metrics", metrics.metrics, name="metrics"),
]
