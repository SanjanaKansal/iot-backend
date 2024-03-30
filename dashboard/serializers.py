from rest_framework import serializers


class HistogramDataInputSerializer(serializers.Serializer):
    client_id = serializers.CharField(max_length=56)
    from_epoch = serializers.IntegerField(required=False)
    to_epoch = serializers.IntegerField(required=False)