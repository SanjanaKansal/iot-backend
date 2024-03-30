from rest_framework import serializers

from .helpers import sanitise_electrical_data, sanitise_water_data
from .models import ElectricalData, WaterData


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
