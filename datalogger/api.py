import random
import time

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from datalogger.models import ClientData, ElectricalData, WaterData, Tag
from datalogger.serializers import (
    ClientDataSerializer,
    ElectricalDataSerializer,
    WaterDataSerializer, TagSerializer,
)


class HealthcheckViewSet(ViewSet):

    def list(self, request, *args, **kwargs):
        data = {
            "status": "ok",
            "message": "Service is up and running."
        }
        return Response(data)


class LoggerViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        client_id = request.data["client_id"]
        type = request.GET.get("type")
        total_days = 200
        samples_per_day = 16
        data = []
        if type == "electrical":
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
            serializer = ElectricalDataSerializer(data=data, many=True)
        elif type == "water":
            for i in range(total_days * samples_per_day):
                data.append(
                    {
                        "client_id": client_id,
                        "time_window_in_seconds": int(random.random()),
                        "flow_rate": random.random(),
                        "volume": random.random(),
                        "timestamp": int(time.time() - i * 900),
                    }
                )
            serializer = WaterDataSerializer(data=data, many=True)
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


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)
