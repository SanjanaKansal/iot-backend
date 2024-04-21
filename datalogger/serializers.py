from rest_framework import serializers

from .helpers import sanitise_electrical_data, sanitise_water_data
from .models import ClientData, ElectricalData, WaterData, Tag


class ElectricalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricalData
        fields = "__all__"

    def create(self, validated_data):
        sanitise_electrical_data(validated_data=validated_data)
        return super().create(validated_data)


class WaterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterData
        fields = "__all__"

    def create(self, validated_data):
        sanitise_water_data(validated_data=validated_data)
        return super().create(validated_data)


class ClientDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientData
        fields = "__all__"


class ClientPhaseSerializer(serializers.Serializer):
    client_id = serializers.CharField()
    phase = serializers.ListField(
        child=serializers.CharField(),
    )


class TagSerializer(serializers.ModelSerializer):
    client_ids = serializers.ListField(
        child=ClientPhaseSerializer(),
        allow_null=True,
        required=False
    )
    class Meta:
        model = Tag
        fields = "__all__"
