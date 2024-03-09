from django.contrib import admin
from . import models


@admin.register(models.Tracker)
class TrackerAdmin(admin.ModelAdmin):
    pass
