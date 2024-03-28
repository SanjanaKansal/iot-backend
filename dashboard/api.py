import time

from django.db.models import Count, Sum
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from dashboard import constants
from dashboard.serializers import HistogramDataInputSerializer
from datalogger.models import ElectricalData


class PowerDashboardViewSet(ModelViewSet):
    serializer_class = HistogramDataInputSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        current_epoch = int(time.time())
        if data["to_epoch"] > current_epoch:
            data["to_epoch"] = current_epoch

        intervals = []
        width = 30
        for i in range(data["from_epoch"], data["to_epoch"]+1, width):
            intervals.append(i)
        client_ids = []
        if data["client_id"] in constants.transformer_panel_PhaseB:
            client_ids = constants.transformer_panel_PhaseB
        elif data["client_id"] in constants.transformer_panel_PhaseR:
            client_ids = constants.transformer_panel_PhaseR
        elif data["client_id"] in constants.transformer_panel_PhaseY:
            client_ids = constants.transformer_panel_PhaseY
        elif data["client_id"] in constants.dg_panel_PhaseB:
            client_ids = constants.dg_panel_PhaseB
        elif data["client_id"] in constants.dg_panel_PhaseR:
            client_ids = constants.dg_panel_PhaseR
        elif data["client_id"] in constants.dg_panel_PhaseY:
            client_ids = constants.dg_panel_PhaseY

        electrical_data = ElectricalData.objects.filter(
            client_id__in=client_ids,
            generation_timestamp__gte=data["from_epoch"],
            generation_timestamp__lt=data["to_epoch"]
        )
        timestamps = []
        values = []

        for i in range(len(intervals)-1):
            lower_interval, upper_interval = intervals[i], intervals[i+1]
            filtered_electrical_data = electrical_data.filter(
                generation_timestamp__gte=lower_interval,
                generation_timestamp__lt=upper_interval
            ).annotate(total_samples=Count("power"), total_power=Sum("power"))
            if filtered_electrical_data:
                sample = filtered_electrical_data[0]
                timestamps.append(upper_interval)
                if sample.total_power > 0:
                    values.append(sample.total_power/sample.total_samples)
                else:
                    values.append(0)
        return Response({"timestamps": timestamps, "values": values})