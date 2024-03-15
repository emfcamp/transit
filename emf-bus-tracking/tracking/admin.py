import xml.etree.ElementTree
import celery.result
import pytz
import csv
import datetime
import codecs
from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin, SortableAdminBase
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
    readonly_fields = ("id",)

    def save_model(self, request, obj: models.Stop, form, change):
        super().save_model(request, obj, form, change)
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
    change_list_template = "tracking/journey_changelist.html"
    inlines = [JourneyPointAdmin]
    list_display = ("code", "route", "start_date")
    readonly_fields = ("start_date", "kalman_estimator_state")
    sortable_by = ("code", "route", "start_date")

    def save_model(self, request, obj: models.Journey, form, change):
        super().save_model(request, obj, form, change)
        gtfs_tasks.generate_gtfs_schedule.delay()

    def get_urls(self):
        urls = super().get_urls()
        urls = [
                   path("import_journey/", self.admin_site.admin_view(self.import_journey),
                        name="tracking_journey_import"),
               ] + urls
        return urls

    def import_journey(self, request):
        if request.method == "POST":
            try:
                self.handle_import(request)
            except ValidationError as e:
                self.message_user(request, e.message, level=messages.ERROR)
            else:
                gtfs_tasks.generate_gtfs_schedule.delay()
                return redirect("admin:tracking_journey_changelist")

        context = dict(
            self.admin_site.each_context(request),
        )
        return TemplateResponse(request, "tracking/journey_import.html", context)

    def get_journey_by_code_and_date(self, code: str, date: datetime.date):
        journey_obj = None

        possible_journey_objs = models.Journey.objects.filter(code=code)
        for possible_journey_obj in possible_journey_objs:
            if point := possible_journey_obj.points.first():
                if point.departure_time.date() == date:
                    journey_obj = possible_journey_obj
                    break

        return journey_obj

    def handle_import(self, request):
        if not request.FILES.get("journey_csv"):
            raise ValidationError("No file uploaded")

        if not request.POST.get("timezone"):
            raise ValidationError("No timezone given")

        try:
            file_timezone = pytz.timezone(request.POST["timezone"])
        except pytz.UnknownTimeZoneError:
            raise ValidationError(f"Invalid timezone: {request.POST['timezone']}")

        journeys_file = request.FILES["journey_csv"]

        try:
            csv_reader = csv.DictReader(codecs.iterdecode(journeys_file, 'utf-8'))
        except csv.Error as e:
            raise ValidationError(f"Invalid CSV: {e}")

        import_required_fields = [
            "Day", "Headcode", "Vehicle", "Route", "From code", "To code", "Depart time", "Arrival time", "Public"
        ]
        if not all(field in csv_reader.fieldnames for field in import_required_fields):
            raise ValidationError(f"Missing required fieldss: {import_required_fields}")

        seen_forms_from = set()

        for journey in csv_reader:
            if not all(journey.get(field) for field in import_required_fields):
                continue

            try:
                service_start_date = file_timezone.localize(
                    timezone.datetime.strptime(journey["Day"], "%d/%m/%Y")
                ).date()
            except ValueError:
                raise ValidationError(f"Invalid date: {journey['Day']}")

            try:
                route = models.Route.objects.get(name=journey["Route"])
            except models.Route.DoesNotExist:
                route = None

            if journey.get("Shape"):
                try:
                    shape = models.Shape.objects.get(name=journey["Shape"])
                except models.Shape.DoesNotExist:
                    raise ValidationError(f"Shape not found: {journey['Shape']}")
            else:
                shape = None

            try:
                vehicle = models.Vehicle.objects.get(name=journey["Vehicle"])
            except models.Vehicle.DoesNotExist:
                raise ValidationError(f"Vehicle not found: {journey['Vehicle']}")

            if journey.get("Forms from"):
                try:
                    forms_from = self.get_journey_by_code_and_date(journey["Forms from"], service_start_date)
                except models.Journey.DoesNotExist:
                    raise ValidationError(f"Forms from journey not found: {journey['Forms from']}")
            else:
                forms_from = None

            if forms_from:
                if (forms_from.id, service_start_date) in seen_forms_from:
                    raise ValidationError(f"Duplicate forms from journey:"
                                          f" {journey['Forms from']} on {service_start_date}")
                seen_forms_from.add((forms_from.id, service_start_date))

            if not journey.get("Direction"):
                direction = models.Journey.DIRECTION_INBOUND
            elif journey["Direction"] == "Inbound":
                direction = models.Journey.DIRECTION_INBOUND
            elif journey["Direction"] == "Outbound":
                direction = models.Journey.DIRECTION_OUTBOUND
            else:
                raise ValidationError(f"Invalid direction: {journey['Direction']}")

            try:
                from_stop = models.Stop.objects.get(code=journey["From code"])
            except models.Stop.DoesNotExist:
                raise ValidationError(f"From stop not found: {journey['From code']}")

            try:
                to_stop = models.Stop.objects.get(code=journey["To code"])
            except models.Stop.DoesNotExist:
                raise ValidationError(f"To stop not found: {journey['To code']}")

            try:
                departure_time = file_timezone.localize(
                    timezone.datetime.strptime(journey["Depart time"], "%H:%M:%S")
                ).time()
            except ValueError:
                raise ValidationError(f"Invalid departure time: {journey['Depart time']}")

            with transaction.atomic():
                journey_obj = self.get_journey_by_code_and_date(journey["Headcode"], service_start_date)
                if not journey_obj:
                    journey_obj = models.Journey(code=journey["Headcode"])

                journey_obj.public = journey["Public"] == "Yes"
                journey_obj.route = route
                journey_obj.vehicle = vehicle
                journey_obj.forms_from = forms_from
                journey_obj.direction = direction
                journey_obj.shape = shape
                journey_obj.save()

                start_point = models.JourneyPoint(
                    journey=journey_obj,
                    stop=from_stop,
                    timing_point=True,
                    order=1,
                    departure_time=file_timezone.localize(timezone.datetime.combine(service_start_date, departure_time))
                )
                end_point = models.JourneyPoint(
                    journey=journey_obj,
                    stop=to_stop,
                    timing_point=True,
                    order=2,
                    arrival_time=file_timezone.localize(timezone.datetime.combine(service_start_date, departure_time))
                )

                journey_obj.points.all().delete()
                start_point.save()
                end_point.save()


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
                   path("update_shape_average_speed/<shape_id>/",
                        self.admin_site.admin_view(self.updae_shape_average_speed),
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
