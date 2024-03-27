from django.db import models


class ElectricalData(models.Model):
    client_id = models.CharField(max_length=56)
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
