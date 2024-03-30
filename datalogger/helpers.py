def sanitise_electrical_data(validated_data):
    if validated_data["phase"] < 0:
        validated_data["phase"] = float(abs(float(validated_data["phase"])))

    if validated_data["current_RMS"] < 0:
        validated_data["current_RMS"] = float(abs(float(validated_data["current_RMS"])))

    if validated_data["power"] < 0:
        validated_data["power"] = abs(validated_data["power"])

    if validated_data["energy"] < 0:
        validated_data["energy"] = abs(validated_data["energy"])


def sanitise_water_data(validated_data):
    if validated_data["flow_rate"] < 0:
        validated_data["flow_rate"] = float(abs(float(validated_data["flow_rate"])))

    if validated_data["flow_rate"] > 100:
        validated_data["flow_rate"] = 30

    if validated_data["volume"] > 100:
        validated_data["volume"] = float(abs(float(validated_data["volume"])))
