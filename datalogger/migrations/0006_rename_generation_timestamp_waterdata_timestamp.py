# Generated by Django 5.0.3 on 2024-04-07 06:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("datalogger", "0005_rename_current_rms_electricaldata_current_rms_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="waterdata",
            old_name="generation_timestamp",
            new_name="timestamp",
        ),
    ]
