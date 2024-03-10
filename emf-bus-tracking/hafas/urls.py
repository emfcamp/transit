from django.urls import path
from . import views

urlpatterns = [
    path("departureBoard", views.departure_board),
]
