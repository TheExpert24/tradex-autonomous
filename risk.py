import numpy as np

MAX_POS = 5
MAX_ALLOCATION = 0.2
THRESHOLD = 1.0

def position_size(signal_value, equity):
    if abs(signal_value) < THRESHOLD:
        return 0

    size = min(abs(signal_value) * 0.1, MAX_ALLOCATION)
    return size * equity

def cap_positions(positions):
    if len(positions) > MAX_POS:
        sorted_keys = sorted(positions.keys(), key=lambda x: abs(positions[x]), reverse=True)
        keep = sorted_keys[:MAX_POS]
        return {k: positions[k] for k in keep}
    return positions