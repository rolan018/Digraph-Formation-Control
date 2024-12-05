"""
Validate control function for sat

control -> f(control) -> validate_control
"""

import numpy as np
from utils import check_size

zero_control = np.array([[0, 0, 0]])
max_control = 0.005

def validate_control(control_iso, deactivated: bool):
    if deactivated:
        return zero_control
    # check valid shape
    check_size(control_iso, (1, 3))
    control = control_iso
    norm_control = float(np.linalg.norm(control_iso))
    if norm_control >= max_control:
        control = control_iso/norm_control * max_control
    return control