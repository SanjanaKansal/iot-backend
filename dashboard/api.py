import time

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet

from dashboard import constants
from dashboard.helpers import get_data_points
from dashboard.models import Config, MetricTypes
from dashboard.serializers import HistogramDataInputSerializer, ConfigSerializer
from datalogger.models import ElectricalData, WaterData, ClientTypes


class DashboardViewSet(ModelViewSet):
    serializer_class = HistogramDataInputSerializer
    queryset = Config.objects.all()

    def __int__(self, type):
        self.type = type

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        timestamps, values = get_data_points(data=data, type=self.type)
        return Response({"timestamps": timestamps, "values": values})

    @action(methods=["GET", "PUT"], detail=False)
    def config(self, request, *args, **kwargs):
        organization_id = request.GET.get("organization_id", "iit-jammu")
        origin = request.GET.get("origin")
        if origin is None:
            return Response(
                {"message": "Origin is required."},
                status=HTTP_400_BAD_REQUEST,
            )
        if request.method == "PUT":
            serializer = ConfigSerializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            for config in data:
                Config.objects.update_or_create(
                    graph_type=config["graph_type"],
                    metric=config["metric"],
                    order=config["order"],
                    defaults={
                        "organization_id": organization_id,
                        "origin": origin
                    }
                )
        configs = Config.objects.filter(organization_id=organization_id, origin=origin)
        data = [{"graph_type": config.graph_type, "metric": config.metric, "order": config.order} for config in configs]
        return Response({"config": data})

    @action(methods=["GET"], detail=False)
    def metric(self, request, *args, **kwargs):
        origin = request.GET.get("origin")
        if origin is None:
            return Response(
                {"message": "Origin is required."},
                status=HTTP_400_BAD_REQUEST,
            )
        data = [
            MetricTypes.VOLTAGE_RMS,
            MetricTypes.CURRENT_RMS,
            MetricTypes.VOLTAGE_PEAK,
            MetricTypes.CURRENT_PEAK,
            MetricTypes.VOLTAGE_FREQUENCY,
            MetricTypes.POWER,
            MetricTypes.ENERGY,
        ] if origin in [ClientTypes.ELECTRICAL_DISTRIBUTION, ClientTypes.ELECTRICAL_GENERATION] else [MetricTypes.FLOW_RATE, MetricTypes.VOLUME]
        return Response(data)

    @action(methods=["GET"], detail=False)
    def data(self, request, *args, **kwargs):
        origin = request.GET.get("origin")
        metric = request.GET.get("metric")
        phases = request.GET.get("phase").split(",")
        clients = request.GET.get("client").split(",")
        if origin is None:
            return Response(
                {"message": "Origin is required."},
                status=HTTP_400_BAD_REQUEST,
            )
        if metric is None:
            return Response(
                {"message": "Metric is required."},
                status=HTTP_400_BAD_REQUEST,
            )
        if clients is None:
            return Response(
                {"message": "Client is required."},
                status=HTTP_400_BAD_REQUEST,
            )
        if phases is None:
            return Response(
                {"message": "Phase is required."},
                status=HTTP_400_BAD_REQUEST,
            )
        from_epoch = request.GET.get("from_epoch")
        to_epoch = request.GET.get("to_epoch")
        current_epoch = int(time.time())

        if not from_epoch:
            from_epoch = current_epoch - 604800
        if not to_epoch:
            to_epoch = current_epoch
        else:
            to_epoch = min(int(to_epoch), current_epoch)
        from_epoch = int(from_epoch)
        to_epoch = int(to_epoch)
        if origin in [ClientTypes.ELECTRICAL_DISTRIBUTION, ClientTypes.ELECTRICAL_GENERATION]:
            query = ElectricalData.objects.all()
        elif origin in [ClientTypes.WATER_DISTRIBUTION, ClientTypes.WATER_GENERATION]:
            query = WaterData.objects.all()
        client_ids = [f"{client}_{phase}" for client in clients for phase in phases]
        results = {}
        for client_id in client_ids:
            client_data = query.filter(
                timestamp__range=[from_epoch, to_epoch], client_id=client_id
            ).values_list("timestamp", metric).order_by("timestamp")

            # Store the result in a dictionary keyed by client_id
            results[client_id] = list(client_data)

        width = 300
        if to_epoch - from_epoch >= 604800:  # 7 days
            width = 7200
        elif to_epoch - from_epoch > 131400 * 60:  # 3 months
            width = 36000

        # Optimize interval creation
        intervals = list(range(from_epoch, to_epoch + 1, width))
        timestamps = intervals[1:]
        client_values = {}
        if results:
            for client_id, db_data in results.items():
                values = [0] * (len(timestamps))
                interval_index = 0
                total_value, total_samples = 0, 0
                for timestamp, data in db_data:
                    # Move to the correct interval for the current timestamp
                    while (
                        interval_index < len(timestamps) - 1
                        and timestamp > timestamps[interval_index]
                    ):
                        if total_samples > 0:
                            values[interval_index] = total_value / total_samples
                        interval_index += 1
                        total_value, total_samples = 0, 0  # Reset for the next interval

                    if timestamps[interval_index - 1] < timestamp <= timestamps[interval_index]:
                        if type in [
                            constants.HistogramDataType.WATER_FLOW,
                            constants.HistogramDataType.WATER_VOLUME,
                        ]:
                            total_value += abs(data)
                        else:
                            total_value += data
                        total_samples += 1

                if total_samples > 0:
                    values[interval_index] = total_value / total_samples
                client_values[client_id] = values

        return Response({"timestamps": timestamps, "values": client_values})


class PowerDashboardViewSet(DashboardViewSet):
    def __init__(self, **kwargs):
        super(PowerDashboardViewSet, self).__init__(**kwargs)
        self.type = constants.HistogramDataType.POWER


class EnergyDashboardViewSet(DashboardViewSet):
    def __init__(self, **kwargs):
        super(EnergyDashboardViewSet, self).__init__(**kwargs)
        self.type = constants.HistogramDataType.ENERGY


class WaterFlowDashboardViewSet(DashboardViewSet):
    def __init__(self, **kwargs):
        super(WaterFlowDashboardViewSet, self).__init__(**kwargs)
        self.type = constants.HistogramDataType.WATER_FLOW


class WaterVolumeDashboardViewSet(DashboardViewSet):
    def __init__(self, **kwargs):
        super(WaterVolumeDashboardViewSet, self).__init__(**kwargs)
        self.type = constants.HistogramDataType.WATER_VOLUME
