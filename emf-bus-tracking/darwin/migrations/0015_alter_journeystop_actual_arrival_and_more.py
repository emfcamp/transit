# Generated by Django 5.0.3 on 2024-03-12 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("darwin", "0014_alter_monitoredstation_linked_stop_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="journeystop",
            name="actual_arrival",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="journeystop",
            name="actual_departure",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="journeystop",
            name="estimated_arrival",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="journeystop",
            name="estimated_departure",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="journeystop",
            name="public_arrival",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="journeystop",
            name="public_departure",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="journeystop",
            name="working_arrival",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="journeystop",
            name="working_departure",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]
