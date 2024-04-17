from django.db import models


class OriginTypes(models.TextChoices):
    POWER_CONSUMPTION = "power_consumption"
    POWER_DISTRIBUTION = "power_distribution"
    WATER = "water"


class MetricTypes(models.TextChoices):
    VOLTAGE_RMS = "voltage_rms"
    CURRENT_RMS = "current_rms"
    VOLTAGE_PEAK = "voltage_peak"
    CURRENT_PEAK = "current_peak"
    VOLTAGE_FREQUENCY = "voltage_frequency"
    POWER = "power"
    ENERGY = "energy"
    FLOW_RATE = "flow_rate"
    VOLUME = "volume"


class Config(models.Model):
    organization_id = models.CharField(max_length=1024)
    origin = models.CharField(choices=OriginTypes.choices, default=OriginTypes.POWER_CONSUMPTION)
    graph_type = models.CharField(max_length=256)
    metric = models.CharField(choices=MetricTypes.choices, default=MetricTypes.VOLTAGE_RMS)
    order = models.IntegerField(default=1)