from django.db import models


class TrainOperatingCompany(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=256)
    website = models.URLField(max_length=512, blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Location(models.Model):
    tiploc = models.CharField(max_length=7, primary_key=True)
    crs = models.CharField(max_length=3, blank=True, null=True)
    toc = models.ForeignKey(
        TrainOperatingCompany, on_delete=models.DO_NOTHING, blank=True, null=True, db_constraint=False,
        verbose_name="Train Operating Company")
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        if self.crs:
            return f"{self.tiploc} ({self.crs}) - {self.name}"
        return f"{self.tiploc} - {self.name}"


class LateRunningReason(models.Model):
    code = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.code} - {self.description}"


class CancellationReason(models.Model):
    code = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.code} - {self.description}"


class Journey(models.Model):
    rtti_unique_id = models.CharField(max_length=16, primary_key=True, verbose_name="RTTI Unique ID")
    uid = models.CharField(max_length=6, verbose_name="UID")
    headcode = models.CharField(max_length=4, verbose_name="Headcode (train ID)")

    date = models.DateField()

    cancel_reason = models.ForeignKey(
        CancellationReason, on_delete=models.DO_NOTHING, db_constraint=False, blank=True, null=True)
    cancel_location = models.ForeignKey(
        Location, on_delete=models.DO_NOTHING, db_constraint=False, blank=True, null=True,
        related_name="cancellation_journeys")
    cancel_reason_near = models.BooleanField(default=False, blank=True)

    late_reason = models.ForeignKey(
        LateRunningReason, on_delete=models.DO_NOTHING, db_constraint=False, blank=True, null=True)
    late_location = models.ForeignKey(
        Location, on_delete=models.DO_NOTHING, db_constraint=False, blank=True, null=True,
        related_name="late_journeys")
    late_reason_near = models.BooleanField(default=False, blank=True)

    toc = models.ForeignKey(
        TrainOperatingCompany, on_delete=models.DO_NOTHING, db_constraint=False,
        verbose_name="Train Operating Company")
    activated = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.headcode}"


class JourneyStop(models.Model):
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, related_name="stops")
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, db_constraint=False)
    order = models.IntegerField()

    origin = models.BooleanField(default=False, blank=True)
    destination = models.BooleanField(default=False, blank=True)

    canceled = models.BooleanField(default=False, blank=True)

    planned_platform = models.CharField(max_length=3, blank=True, null=True)
    current_platform = models.CharField(max_length=3, blank=True, null=True)
    platform_suppressed = models.BooleanField(default=False, blank=True)
    platform_confirmed = models.BooleanField(default=False, blank=True)

    supress = models.BooleanField(default=False, blank=True)

    public_arrival = models.TimeField(blank=True, null=True)
    public_departure = models.TimeField(blank=True, null=True)

    working_arrival = models.TimeField(blank=True, null=True)
    working_departure = models.TimeField(blank=True, null=True)

    actual_arrival = models.TimeField(blank=True, null=True)
    actual_departure = models.TimeField(blank=True, null=True)

    estimated_arrival = models.TimeField(blank=True, null=True)
    estimated_departure = models.TimeField(blank=True, null=True)

    unknown_delay_arrival = models.BooleanField(default=False, blank=True)
    unknown_delay_departure = models.BooleanField(default=False, blank=True)

    use_false_destination = models.BooleanField(default=False, blank=True)

    class Meta:
        unique_together = ("journey", "location", "order")
        ordering = ("order",)

    def __str__(self):
        return f"{self.journey} - {self.location}"


class Message(models.Model):
    message_id = models.IntegerField(primary_key=True)
    message = models.TextField()
    category = models.CharField(max_length=255)
    severity = models.CharField(max_length=255)
    supress_rtt = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.message_id}"


class MessageStation(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="stations")
    crs = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.message} - {self.crs}"


class MonitoredStation(models.Model):
    crs = models.CharField(max_length=3, verbose_name="CRS code (station identifier)")

    def location(self):
        return Location.objects.filter(crs=self.crs).first()

    def __str__(self):
        location = self.location()
        if location:
            return f"{self.crs} - {location.name}"
        return f"{self.crs} - Unknown location"

