from django.urls import path
from . import views

urlpatterns = [
    path("location.name", views.location_search_by_name),
    path("arrivalBoard", views.arrival_board),
    path("departureBoard", views.departure_board),
]
