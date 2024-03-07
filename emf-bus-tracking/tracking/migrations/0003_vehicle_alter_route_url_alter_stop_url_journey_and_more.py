# Generated by Django 5.0.1 on 2024-01-25 16:04

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracking", "0002_route_stop_internal_stop_url_alter_stop_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Vehicle",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("registration_plate", models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name="route",
            name="url",
            field=models.URLField(blank=True, null=True, verbose_name="URL"),
        ),
        migrations.AlterField(
            model_name="stop",
            name="url",
            field=models.URLField(blank=True, null=True, verbose_name="URL"),
        ),
        migrations.CreateModel(
            name="Journey",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("code", models.CharField(max_length=255)),
                (
                    "direction",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Inbound"), (1, "Outbound")]
                    ),
                ),
                ("date", models.DateField()),
                ("public", models.BooleanField(blank=True, default=True)),
                (
                    "forms_from",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="forms_to",
                        to="tracking.journey",
                    ),
                ),
                (
                    "route",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="tracking.route",
                    ),
                ),
                (
                    "vehicle",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="tracking.vehicle",
                    ),
                ),
            ],
            options={
                "ordering": ["date", "code"],
                "unique_together": {("code", "date")},
            },
        ),
        migrations.CreateModel(
            name="JourneyPoint",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("arrival_time", models.TimeField(blank=True, null=True)),
                ("departure_time", models.TimeField()),
                ("timing_point", models.BooleanField(blank=True, default=True)),
                ("order", models.PositiveIntegerField(blank=True, default=0)),
                (
                    "journey",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tracking.journey",
                    ),
                ),
                (
                    "stop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tracking.stop"
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
            },
        ),
    ]
