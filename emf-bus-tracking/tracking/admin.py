import xml.etree.ElementTree

import celery.result
from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin, SortableAdminBase
from django.core.checks import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.urls import path
from django.utils import timezone
from django.contrib import messages
from gtfs import gtfs_tasks
from . import models, os_average_speed


@admin.register(models.Stop)
class StopAdmin(admin.ModelAdmin):
    def save_model(self, request, obj: models.Stop, form, change):
        super().save_model(request, obj, form, change)
        if not obj.internal:
            gtfs_tasks.generate_gtfs_schedule.delay()


class VehiclePositionAdmin(admin.TabularInline):
    model = models.VehiclePosition


@admin.register(models.Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    inlines = [VehiclePositionAdmin]


@admin.register(models.Route)
class RouteAdmin(SortableAdminMixin, admin.ModelAdmin):
    def save_model(self, request, obj: models.Route, form, change):
        super().save_model(request, obj, form, change)
        gtfs_tasks.generate_gtfs_schedule.delay()


class JourneyPointAdmin(SortableInlineAdminMixin, admin.TabularInline):
    model = models.JourneyPoint
    readonly_fields = ["real_time_arrival", "real_time_departure", "estimated_arrival", "estimated_departure"]


@admin.register(models.Journey)
class JourneyAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [JourneyPointAdmin]

    def save_model(self, request, obj: models.Journey, form, change):
        super().save_model(request, obj, form, change)

        if obj.public:
            gtfs_tasks.generate_gtfs_schedule.delay()


@admin.register(models.Shape)
class ShapeAdmin(SortableAdminBase, admin.ModelAdmin):
    readonly_fields = ["last_average_speed_update"]
    change_list_template = "tracking/shape_changelist.html"
    change_form_template = "tracking/shape_change.html"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        gtfs_tasks.generate_gtfs_schedule.delay()

    def get_urls(self):
        urls = super().get_urls()
        urls = [
            path("import_shape/", self.admin_site.admin_view(self.import_shape), name="tracking_shape_import"),
            path("update_shape_average_speed/<shape_id>/", self.admin_site.admin_view(self.updae_shape_average_speed),
                 name="tracking_shape_update_average_speed"),
        ] + urls
        return urls

    def import_shape(self, request):
        if request.method == "POST":
            try:
                self.handle_import(request)
            except ValidationError as e:
                self.message_user(request, e.message, level=messages.ERROR)
            else:
                return redirect("admin:tracking_shape_changelist")

        context = dict(
            self.admin_site.each_context(request),
        )
        return TemplateResponse(request, "tracking/shape_import.html", context)

    def handle_import(self, request):
        if not request.FILES.get("kml_file"):
            raise ValidationError("No file uploaded")

        file = request.FILES["kml_file"]
        try:
            d = xml.etree.ElementTree.fromstring(file.read())
        except xml.etree.ElementTree.ParseError:
            raise ValidationError("Invalid XML")

        namespaces = {
            "kml": "http://www.opengis.net/kml/2.2"
        }

        placemarks = d.findall("kml:Document/kml:Placemark", namespaces=namespaces)
        if not placemarks:
            raise ValidationError("No Placemarks found")

        name = None
        line_string = None
        for placemark in placemarks:
            name = placemark.find("kml:name", namespaces=namespaces)
            line_string = placemark.find("kml:LineString", namespaces=namespaces)
            if line_string is not None:
                break

        if line_string is None:
            raise ValidationError("No LineString found")

        coordinates = line_string.find("kml:coordinates", namespaces=namespaces)
        coordinates = coordinates.text.strip().split("\n")

        if not coordinates:
            raise ValidationError("No coordinates found")

        with transaction.atomic():
            shape = models.Shape.objects.create(name=name.text.strip() if name is not None else "Unnamed")
            for i, coordinate in enumerate(coordinates):
                coordinate = coordinate.strip()
                parts = coordinate.split(',')
                if len(parts) != 3:
                    raise ValidationError(f"Invalid coordinate: {coordinate}")
                long, lat, _ = parts
                lat = float(lat)
                long = float(long)
                models.ShapePoint.objects.create(
                    shape=shape,
                    latitude=lat,
                    longitude=long,
                    order=i,
                )

    def updae_shape_average_speed(self, request, shape_id):
        shape = get_object_or_404(self.model, id=shape_id)

        pending = False

        if "update_average_speed_task_id" in request.session:
            start = request.session.get("update_average_speed_task_start", 0)
            if timezone.now().timestamp() - start > 600:
                messages.add_message(request, messages.ERROR, "Task took too long to complete")
                del request.session["update_average_speed_task_id"]
                del request.session["update_average_speed_task_start"]
                pending = False
            else:
                pending = True
                result = celery.result.AsyncResult(request.session["update_average_speed_task_id"])
                if result.status == "SUCCESS":
                    result_message = result.result
                    if result_message:
                        messages.add_message(request, messages.ERROR, result_message)
                    else:
                        messages.add_message(request, messages.INFO, "Update successful")
                elif result.status == "FAILURE":
                    messages.add_message(request, messages.ERROR, "Update failed")

                if result.status in ("SUCCESS", "FAILURE"):
                    del request.session["update_average_speed_task_id"]
                    del request.session["update_average_speed_task_start"]
                    return redirect(
                        f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
                        shape.id
                    )

        if not pending:
            if request.method == "POST":
                result = os_average_speed.update_average_speed_data.delay(shape.id)
                request.session["update_average_speed_task_id"] = result.id
                request.session["update_average_speed_task_start"] = timezone.now().timestamp()
                return redirect(request.path)

        context = dict(
            self.admin_site.each_context(request),
            opts=self.model._meta,
            object_id=shape_id,
            pending=pending,
        )
        return TemplateResponse(request, "tracking/shape_update_average_speed_data.html", context)


class ServiceAlertPeriodAdmin(admin.TabularInline):
    model = models.ServiceAlertPeriod


class ServiceAlertSelectorAdmin(admin.TabularInline):
    model = models.ServiceAlertSelector


@admin.register(models.ServiceAlert)
class ServiceAlertAdmin(admin.ModelAdmin):
    inlines = [ServiceAlertPeriodAdmin, ServiceAlertSelectorAdmin]


@admin.register(models.Tracker)
class TrackerAdmin(admin.ModelAdmin):
    pass
