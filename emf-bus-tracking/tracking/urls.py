from django.urls import path, register_converter
from . import views, metrics, vehicle_sheets, converters

register_converter(converters.DateConverter, 'date')

urlpatterns = [
    path("", views.index, name="index"),
    path("metrics", metrics.metrics, name="metrics"),
    path("vehicle_sheet/<uuid:vehicle_id>/<date:service_date>/", vehicle_sheets.vehicle_sheet, name="vehicle_sheet"),
]
