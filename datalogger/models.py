from django.db import models


class ElectricalData(models.Model):
    client_id = models.TextField()
    timestamp = models.IntegerField()
    voltage_rms = models.FloatField()
    current_rms = models.FloatField()
    voltage_peak = models.FloatField(null=True)
    current_peak = models.FloatField(null=True)
    phase = models.FloatField()
    voltage_frequency = models.FloatField()
    power = models.FloatField()
    energy = models.FloatField()
    watt_hour = models.FloatField(null=True)
    total_watts = models.FloatField(null=True)
    delete_status = models.BooleanField(default=False)


class VolumeUnitTypes(models.TextChoices):
    ML = "ml"
    L = "l"
    KL = "kl"


class RateTypes(models.TextChoices):
    SEC = "sec"
    MIN = "min"
    HOUR = "hour"


class WaterData(models.Model):
    client_id = models.CharField(max_length=56)
    timestamp = models.IntegerField()
    flow_rate = models.FloatField()
    time_window_in_seconds = models.IntegerField()
    volume = models.FloatField()
    rate_unit = models.CharField(choices=RateTypes.choices, default=RateTypes.SEC)
    volume_unit = models.CharField(choices=VolumeUnitTypes.choices, default=VolumeUnitTypes.ML)


class ClientTypes(models.TextChoices):
    ELECTRICAL_DISTRIBUTION = "electrical_distribution"
    ELECTRICAL_GENERATION = "electrical_generation"
    WATER_DISTRIBUTION = "water_distribution"
    WATER_GENERATION = "water_generation"


class ClientData(models.Model):
    organization_id = models.CharField(max_length=256)
    organization_label = models.CharField(max_length=256)
    block_id = models.CharField(max_length=256)
    block_label = models.CharField(max_length=256)
    panel_id = models.CharField(max_length=256)
    panel_label = models.CharField(max_length=256)
    phase_id = models.CharField(max_length=256)
    phase_label = models.CharField(max_length=256)
    client_id = models.CharField(max_length=256)
    client_label = models.CharField(max_length=256)
    client_type = models.CharField(choices=ClientTypes.choices, default=ClientTypes.ELECTRICAL_DISTRIBUTION)
    description = models.CharField(max_length=1024, null=True)
    is_active = models.BooleanField(default=True)
    is_enabled = models.BooleanField(default=True)
    is_faulty = models.BooleanField(default=False)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)