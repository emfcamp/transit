from django.urls import path
from . import views

urlpatterns = [
    path("webhooks", views.kosmos_webhook, name="kosmos_webhook"),
]
