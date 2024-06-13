from rest_framework import serializers

from dashboard.models import Config


class HistogramDataInputSerializer(serializers.Serializer):
    client_id = serializers.CharField(max_length=56)
    from_epoch = serializers.IntegerField(required=False)
    to_epoch = serializers.IntegerField(required=False)


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ("id", "graph_type", "metric", "order", "client", "tag", "name")
