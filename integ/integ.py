"""
Integration function
"""

import numpy as np
from utils import check_size


def pk_4(vec, get_f, control, params, h: int = 1):

    x0 = vec[:3, 0].reshape((1, 3))
    v0 = vec[3:, 0].reshape((1, 3))

    # check shape
    check_size(vec, (6, 1))

    # validate func vector
    check_size(get_f(x0, params), (1, 3))

    # validate control vector
    check_size(control, (1, 3))

    k1 = np.append(v0, get_f(x0, params) + control, axis=1)
    k2 = np.append(
        v0 + k1[0, 3:] * h / 2, get_f(x0 + k1[0, :3] * h / 2, params) + control, axis=1
    )

    k3 = np.append(
        v0 + k2[0, 3:] * h / 2, get_f(x0 + k2[0, :3] * h / 2, params) + control, axis=1
    )

    k4 = np.append(
        v0 + k3[0, 3:] * h, get_f(x0 + k3[0, :3] * h, params) + control, axis=1
    )

    return vec.reshape((1, 6)) + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
