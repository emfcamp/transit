# Generated by Django 5.0.3 on 2024-03-13 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("darwin", "0015_alter_journeystop_actual_arrival_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cancellationreason",
            name="code",
            field=models.IntegerField(db_index=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="laterunningreason",
            name="code",
            field=models.IntegerField(db_index=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="location",
            name="crs",
            field=models.CharField(blank=True, db_index=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name="location",
            name="tiploc",
            field=models.CharField(
                db_index=True, max_length=7, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="messagestation",
            name="crs",
            field=models.CharField(db_index=True, max_length=3),
        ),
        migrations.AlterField(
            model_name="monitoredstation",
            name="crs",
            field=models.CharField(
                db_index=True,
                max_length=3,
                verbose_name="CRS code (station identifier)",
            ),
        ),
        migrations.AlterField(
            model_name="trainoperatingcompany",
            name="code",
            field=models.CharField(
                db_index=True, max_length=2, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="welshstationname",
            name="crs",
            field=models.CharField(
                db_index=True, max_length=3, primary_key=True, serialize=False
            ),
        ),
        migrations.AddIndex(
            model_name="journeystop",
            index=models.Index(
                fields=["journey", "order"], name="darwin_jour_journey_54cb72_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="journeystop",
            index=models.Index(
                fields=["journey", "origin"], name="darwin_jour_journey_eae79a_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="journeystop",
            index=models.Index(
                fields=["journey", "destination"], name="darwin_jour_journey_0bb071_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="journeystop",
            index=models.Index(
                fields=["location", "public_arrival"],
                name="darwin_jour_locatio_c0c1d4_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="journeystop",
            index=models.Index(
                fields=["location", "public_departure"],
                name="darwin_jour_locatio_db52a1_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="journeystop",
            index=models.Index(
                fields=["location", "working_arrival"],
                name="darwin_jour_locatio_da41b9_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="journeystop",
            index=models.Index(
                fields=["location", "working_departure"],
                name="darwin_jour_locatio_910955_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="journeystop",
            index=models.Index(
                fields=["location", "actual_arrival"],
                name="darwin_jour_locatio_2fb277_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="journeystop",
            index=models.Index(
                fields=["location", "actual_departure"],
                name="darwin_jour_locatio_8d9028_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="journeystop",
            index=models.Index(
                fields=["location", "estimated_arrival"],
                name="darwin_jour_locatio_4ddc77_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="journeystop",
            index=models.Index(
                fields=["location", "estimated_departure"],
                name="darwin_jour_locatio_c7bdd7_idx",
            ),
        ),
    ]
