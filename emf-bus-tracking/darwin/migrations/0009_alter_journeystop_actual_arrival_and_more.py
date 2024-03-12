# Generated by Django 5.0.3 on 2024-03-12 12:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("darwin", "0008_alter_trainoperatingcompany_options_and_more"),
        ("tracking", "0013_remove_vehicle_tracker_alter_journey_vehicle_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="journeystop", name="actual_arrival"),
        migrations.AddField(
            model_name="journeystop",
            name="actual_arrival",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RemoveField(model_name="journeystop", name="actual_departure"),
        migrations.AddField(
            model_name="journeystop",
            name="actual_departure",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RemoveField(model_name="journeystop", name="estimated_arrival"),
        migrations.AddField(
            model_name="journeystop",
            name="estimated_arrival",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RemoveField(model_name="journeystop", name="estimated_departure"),
        migrations.AddField(
            model_name="journeystop",
            name="estimated_departure",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RemoveField(model_name="journeystop", name="public_arrival"),
        migrations.AddField(
            model_name="journeystop",
            name="public_arrival",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RemoveField(model_name="journeystop", name="public_departure"),
        migrations.AddField(
            model_name="journeystop",
            name="public_departure",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RemoveField(model_name="journeystop", name="working_arrival"),
        migrations.AddField(
            model_name="journeystop",
            name="working_arrival",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RemoveField(model_name="journeystop", name="working_departure"),
        migrations.AddField(
            model_name="journeystop",
            name="working_departure",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="monitoredstation",
            name="linked_stop",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="darwin_link",
                to="tracking.stop",
            ),
        ),
    ]