"""
Used for manual data from 'data' directory
"""
import numpy as np
import pandas as pd
from sat import Sat, SatType, SatTypeRaft
from params import Params, ReferenceOrbit
from initiator.position import init_position_for_line, init_position
from initiator.velocity import init_velocity

class SatReader:
    def __init__(self, ref_orbit: ReferenceOrbit, params: Params):
        self.ref_orbit = ref_orbit
        self.params = params
        self.sat_list: list[Sat] = []
    
    def read_data(self, file_path: str) -> list[Sat]:
        df = pd.read_csv(file_path, sep=",")
        _, row = next(df.iterrows())
        for sat_enum in (SatType, SatTypeRaft):
            try:
                sat_type = sat_enum.from_str(row["sat_type"])
                break
            except:
                continue
        for _, row in df.iterrows():
            x = np.array([[row["x0"], row["y0"], row["z0"]]]).reshape(3, 1)
            v = np.array([[row["vx0"], row["vy0"], row["vz0"]]]).reshape(3, 1)
            sat_type = sat_enum.from_str(row["sat_type"])
            self.sat_list.append(Sat(x, v, sat_type, self.ref_orbit, self.params))
        return self.sat_list

    def generate_data(self, num_sats, pos_for_line: bool, is_raft: bool) -> list[Sat]:
        pos = init_position
        if pos_for_line:
            pos = init_position_for_line
        for index, (position, velocity) in enumerate(zip(pos(num_sats), init_velocity(num_sats))):
            if is_raft:
                self.sat_list.append(Sat(position, velocity, SatTypeRaft.FOLLOWER, self.ref_orbit, self.params))
            else:
                sat_type = SatType.SECONDARY
                # Add MAIN Sat
                if index in (2, 4):
                    sat_type = SatType.MAIN
                self.sat_list.append(Sat(position, velocity, sat_type, self.ref_orbit, self.params))
        return self.sat_list