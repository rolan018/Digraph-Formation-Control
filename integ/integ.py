"""
Integration function
"""
import numpy as np


def pk_4(vec, get_f, upr, params, h):
    x0 = vec[0, :3].reshape((1, 3))
    print(f"pk_4 x0:{x0}")
    v0 = vec[0, 3:].reshape((1, 3))
    print(f"pk_4 v0:{v0}")

    k1 = np.append(v0,
                   get_f(x0, params) + upr, axis=1)
    print(f"pk_4 k1:{k1}")

    k2 = np.append(v0 + k1[0, 3:] * h / 2,
                   get_f(x0 + k1[0, :3] * h / 2, params) + upr, axis=1)

    k3 = np.append(v0 + k2[0, 3:] * h / 2,
                   get_f(x0 + k2[0, :3] * h / 2, params) + upr, axis=1)

    k4 = np.append(v0 + k3[0, 3:] * h,
                   get_f(x0 + k3[0, :3] * h, params) + upr, axis=1)

    vec_1 = vec + h/6 * (k1 + 2 * k2 + 2 * k3 + k4)
    print(f"pk_4 vec_1:{vec_1}")
    return vec_1
