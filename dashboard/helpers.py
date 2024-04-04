import time


from dashboard import constants
from datalogger.models import ElectricalData, WaterData


def get_data_points(data, type):
    current_epoch = int(time.time())
    if not data.get("from_epoch"):
        data["from_epoch"] = current_epoch - 604800
    if not data.get("to_epoch"):
        data["to_epoch"] = current_epoch
    else:
        data["to_epoch"] = min(data["to_epoch"], current_epoch)

    width = 30
    if data["to_epoch"] - data["from_epoch"] > 604800:  # 7 days
        width = 300    # 5 min
    elif data["to_epoch"] - data["from_epoch"] > 131400 * 60:  # 3 months
        width = 3600   # 1 hr

    # Optimize interval creation
    intervals = list(range(data["from_epoch"], data["to_epoch"] + 1, width))

    # Optimize client_id checks by using a dictionary
    client_id_mapping = {
        **dict.fromkeys(
            constants.transformer_panel_PhaseB, constants.transformer_panel_PhaseB
        ),
        **dict.fromkeys(
            constants.transformer_panel_PhaseR, constants.transformer_panel_PhaseR
        ),
        **dict.fromkeys(
            constants.transformer_panel_PhaseY, constants.transformer_panel_PhaseY
        ),
        **dict.fromkeys(constants.dg_panel_PhaseB, constants.dg_panel_PhaseB),
        **dict.fromkeys(constants.dg_panel_PhaseR, constants.dg_panel_PhaseR),
        **dict.fromkeys(constants.dg_panel_PhaseY, constants.dg_panel_PhaseY),
    }
    client_ids = client_id_mapping.get(data["client_id"], [])

    db_data = get_db_data(data=data, client_ids=client_ids, histogram_type=type)

    timestamps = intervals[1:]
    values = [0] * (len(timestamps))
    if db_data:
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

    return timestamps, values


def get_db_data(data, client_ids, histogram_type):
    field = None
    model = None
    if histogram_type == constants.HistogramDataType.POWER:
        field = "power"
        model = ElectricalData
    elif histogram_type == constants.HistogramDataType.ENERGY:
        field = "energy"
        model = ElectricalData
    elif histogram_type == constants.HistogramDataType.WATER_FLOW:
        field = "flow_rate"
        model = WaterData
    elif histogram_type == constants.HistogramDataType.WATER_VOLUME:
        field = "volume"
        model = WaterData
    return (
        model.objects.filter(
            generation_timestamp__range=[data["from_epoch"], data["to_epoch"]],
            client_id__in=client_ids,
        )
        .values_list("generation_timestamp", field)
        .order_by("generation_timestamp")
    )
