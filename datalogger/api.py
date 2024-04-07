import random
import time

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from datalogger.models import ClientData, ElectricalData, WaterData
from datalogger.serializers import (
    ClientDataSerializer,
    ElectricalDataSerializer,
    WaterDataSerializer,
)


class LoggerViewSet(ModelViewSet):
    serializer_class = ElectricalDataSerializer
    queryset = ElectricalData.objects.all()

    def create(self, request, *args, **kwargs):
        client_id = request.data["client_id"]
        total_days = 200
        samples_per_day = 16
        data = []
        for i in range(total_days * samples_per_day):
            voltage_rms = 200.0 + 40 * random.random()
            current_rms = 25 * random.random()
            data.append(
                {
                    "client_id": client_id,
                    "voltage_rms": voltage_rms,
                    "current_rms": current_rms,
                    "phase": random.random(),
                    "voltage_frequency": random.random(),
                    "power": float(voltage_rms * current_rms) / 1000,
                    "energy": float(voltage_rms * current_rms) / 4000,
                    "timestamp": int(time.time() - i * 900),
                }
            )
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)


class ElectricalLoggerViewSet(ModelViewSet):
    serializer_class = ElectricalDataSerializer
    queryset = ElectricalData.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)


class WaterLoggerViewSet(ModelViewSet):
    serializer_class = WaterDataSerializer
    queryset = WaterData.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)


class ClientDashboardViewSet(ModelViewSet):
    serializer_class = ClientDataSerializer
    queryset = ClientData.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
