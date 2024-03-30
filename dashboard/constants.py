import enum

transformer_panel_PhaseB = [
    "source_panel_1_103_phase_b",
    "source_panel_1_104_phase_b",
]

transformer_panel_PhaseR = [
    "source_panel_1_103_phase_r",
    "source_panel_1_104_phase_r",
]

transformer_panel_PhaseY = [
    "source_panel_1_103_phase_y",
    "source_panel_1_104_phase_y",
]

dg_panel_PhaseB = [
    "source_panel_1_102_phase_b",
    "source_panel_1_105_phase_b",
]

dg_panel_PhaseR = [
    "source_panel_1_105_phase_r",
    "source_panel_1_102_phase_r",
]

dg_panel_PhaseY = [
    "source_panel_1_105_phase_y",
    "source_panel_1_102_phase_y",
]


class HistogramDataType(enum.Enum):
    POWER = 1
    ENERGY = 2
    WATER_FLOW = 3
    WATER_VOLUME = 4
