import time

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from dashboard import constants
from dashboard.helpers import get_data_points
from dashboard.serializers import HistogramDataInputSerializer


class DashboardViewSet(ModelViewSet):
    serializer_class = HistogramDataInputSerializer

    def __int__(self, type):
        self.type = type

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        timestamps, values = get_data_points(data=data, type=self.type)
        return Response({"timestamps": timestamps, "values": values})


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
