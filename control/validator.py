"""
Validate control function for sat

control -> f(control) -> validate_control
"""

import numpy as np
from utils import check_size

def validate_control(control_iso):
    max_control = 0.005
    # check valid shape
    check_size(control_iso, (1, 3))
    control = control_iso
    norm_control = float(np.linalg.norm(control_iso))
    if norm_control >= max_control:
        control = control_iso/norm_control * max_control
    return control