# Generated by Django 5.0.1 on 2024-01-25 22:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "tracking",
            "0007_servicealert_servicealertperiod_servicealertselector_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="servicealert",
            name="cause",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[
                    (2, "Other cause"),
                    (3, "Technical problem"),
                    (4, "Strike"),
                    (5, "Demonstration"),
                    (6, "Accident"),
                    (7, "Holiday"),
                    (8, "Weather"),
                    (9, "Maintenance"),
                    (10, "Construction"),
                    (11, "Police activity"),
                    (12, "Medical emergency"),
                ],
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="servicealert",
            name="effect",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[
                    (1, "No service"),
                    (2, "Reduced service"),
                    (3, "Significant delays"),
                    (4, "Detour"),
                    (5, "Additional service"),
                    (6, "Modified service"),
                    (7, "Other effect"),
                    (9, "Stop moved"),
                    (10, "No effect"),
                    (11, "Accessibility issue"),
                ],
                null=True,
            ),
        ),
    ]
