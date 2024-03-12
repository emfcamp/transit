# Generated by Django 5.0.3 on 2024-03-12 11:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "darwin",
            "0007_message_rename_platform_journeystop_current_platform_and_more",
        ),
        ("tracking", "0013_remove_vehicle_tracker_alter_journey_vehicle_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="trainoperatingcompany",
            options={
                "verbose_name": "Train Operating Company",
                "verbose_name_plural": "Train Operating Companies",
            },
        ),
        migrations.AddField(
            model_name="monitoredstation",
            name="linked_stop",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="tracking.stop",
            ),
        ),
    ]
