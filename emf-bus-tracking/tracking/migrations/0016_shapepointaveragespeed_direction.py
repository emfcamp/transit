# Generated by Django 5.0.3 on 2024-03-15 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tracking", "0015_alter_journeypoint_arrival_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="shapepointaveragespeed",
            name="direction",
            field=models.PositiveSmallIntegerField(
                choices=[(0, "Forward"), (1, "Reverse")], default=0
            ),
        ),
    ]