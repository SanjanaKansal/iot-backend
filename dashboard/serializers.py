from rest_framework import serializers

from dashboard.models import MetricTypes


class HistogramDataInputSerializer(serializers.Serializer):
    client_id = serializers.CharField(max_length=56)
    from_epoch = serializers.IntegerField(required=False)
    to_epoch = serializers.IntegerField(required=False)


class ConfigSerializer(serializers.Serializer):
    graph_type = serializers.CharField(required=True)
    metric = serializers.ChoiceField(required=True, choices=MetricTypes.choices)
    order = serializers.IntegerField(required=True)