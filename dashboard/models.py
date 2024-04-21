from django.contrib.postgres.fields import ArrayField
from django.db import models

from datalogger.models import ClientTypes, Tag


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
    organization_id = models.CharField(max_length=1024, default="iit-jammu")
    origin = models.CharField(choices=ClientTypes.choices, default=ClientTypes.ELECTRICAL_DISTRIBUTION)
    graph_type = models.CharField(max_length=256)
    metric = models.CharField(choices=MetricTypes.choices, default=MetricTypes.VOLTAGE_RMS)
    order = models.IntegerField(default=1)
    client = models.JSONField(null=True)
    tag = models.IntegerField(null=True)