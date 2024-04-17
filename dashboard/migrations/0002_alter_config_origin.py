# Generated by Django 5.0.3 on 2024-04-15 13:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="config",
            name="origin",
            field=models.CharField(
                choices=[
                    ("power_consumption", "Power Consumption"),
                    ("power_distribution", "Power Distribution"),
                    ("water", "Water"),
                ],
                default="power_consumption",
            ),
        ),
    ]
