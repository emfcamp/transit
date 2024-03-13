from django.contrib import admin
from django.core.checks import messages
from django.shortcuts import redirect
from django.urls import path
from django.contrib import messages
from . import models, tasks


@admin.register(models.TrainOperatingCompany)
class TrainOperatingCompanyAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("code",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("tiploc", "crs", "name")
    search_fields = ("tiploc", "crs", "name")
    ordering = ("tiploc",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(models.LateRunningReason)
class LateRunningReasonAdmin(admin.ModelAdmin):
    list_display = ("code", "description")
    search_fields = ("code", "description")
    ordering = ("code",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(models.CancellationReason)
class CancellationReasonAdmin(admin.ModelAdmin):
    list_display = ("code", "description")
    search_fields = ("code", "description")
    ordering = ("code",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class JourneyStopAdmin(admin.StackedInline):
    model = models.JourneyStop
    extra = 0
    ordering = ("order",)
    exclude = ("order",)


@admin.register(models.Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ("date", "rtti_unique_id", "uid", "headcode",)
    search_fields = ("rtti_unique_id", "uid", "headcode",)
    ordering = ("rtti_unique_id", "uid", "headcode",)
    inlines = (JourneyStopAdmin,)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class MessageStationAdmin(admin.TabularInline):
    model = models.MessageStation
    extra = 0


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("message_id", "category", "severity", "supress_rtt")
    inlines = (MessageStationAdmin,)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True


@admin.register(models.WelshStationName)
class WelshStationNameAdmin(admin.ModelAdmin):
    list_display = ("crs", "name")
    search_fields = ("crs", "name")
    ordering = ("crs",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(models.WelshTrainOperatingCompanyName)
class WelshTrainOperatingCompanyNameAdmin(admin.ModelAdmin):
    list_display = ("toc", "name")
    search_fields = ("toc", "name")
    ordering = ("toc",)


@admin.register(models.MonitoredStation)
class MonitoredStationAdmin(admin.ModelAdmin):
    list_display = ("crs", "location")
    search_fields = ("crs",)
    ordering = ("crs",)

    change_list_template = "darwin/monitored_station_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        urls = [
            path("darwin_sync/", self.admin_site.admin_view(self.darwin_sync), name="darwin_monitoredstation_darwin-sync"),
        ] + urls
        return urls

    @staticmethod
    def darwin_sync(request):
        tasks.sync_tt_files.delay()
        messages.add_message(request, messages.INFO, "Darwin sync scheduled")
        return redirect("admin:darwin_monitoredstation_changelist")
