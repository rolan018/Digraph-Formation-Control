import numpy as np

def printer_init_vector(sats):
    norm_position = []
    norm_velocity = []
    for i in range(len(sats)):
        for j in range(i+1, len(sats)):
            sat_i_p = sats[i].get_position(-1, "osk")
            sat_j_p = sats[j].get_position(-1, "osk")
            sat_i_v = sats[i].get_velocity(-1, "osk")
            sat_j_v = sats[j].get_velocity(-1, "osk")
            norm_position.append((i, j, float(np.linalg.norm(sat_i_p - sat_j_p))))
            norm_velocity.append((i, j, float(np.linalg.norm(sat_i_v - sat_j_v))))
    print("Max X:", max(norm_position, key=lambda item: item[-1]))
    print("Max V:", max(norm_velocity, key=lambda item: item[-1]))
    print("Min X:", min(norm_position, key=lambda item: item[-1]))
    print("Min V:", min(norm_velocity, key=lambda item: item[-1]))