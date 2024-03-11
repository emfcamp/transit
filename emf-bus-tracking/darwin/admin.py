from django.contrib import admin
from . import models


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


class JourneyStopAdmin(admin.TabularInline):
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
        return False


@admin.register(models.MonitoredStation)
class MonitoredStationAdmin(admin.ModelAdmin):
    list_display = ("crs", "location")
    search_fields = ("crs",)
    ordering = ("crs",)
