from django.db import models


class ElectricalData(models.Model):
    client_id = models.TextField()
    generation_timestamp = models.IntegerField()
    voltage_RMS = models.FloatField()
    current_RMS = models.FloatField()
    voltage_peak = models.FloatField(null=True)
    current_peak = models.FloatField(null=True)
    phase = models.FloatField()
    voltage_frequency = models.FloatField()
    power = models.FloatField()
    energy = models.FloatField()
    watt_hour = models.FloatField(null=True)
    total_watts = models.FloatField(null=True)
    delete_status = models.BooleanField(default=False)


class WaterData(models.Model):
    client_id = models.CharField(max_length=56)
    generation_timestamp = models.IntegerField()
    flow_rate = models.FloatField()
    time_window_in_seconds = models.IntegerField()
    volume = models.FloatField()


class ClientData(models.Model):
    organisation_id = models.CharField(max_length=256)
    organisation_label = models.CharField(max_length=256)
    block_id = models.CharField(max_length=256)
    block_label = models.CharField(max_length=256)
    panel_id = models.CharField(max_length=256)
    panel_label = models.CharField(max_length=256)
    level_id = models.CharField(max_length=256)
    level_label = models.CharField(max_length=256)
    phase_id = models.CharField(max_length=256)
    phase_label = models.CharField(max_length=256)
    client_id = models.CharField(max_length=256)
    client_label = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    tags = models.CharField(max_length=1024)
    is_active = models.BooleanField(default=True)
    is_enabled = models.BooleanField(default=True)
    is_faulty = models.BooleanField(default=False)
    last_data_reported = models.IntegerField()
