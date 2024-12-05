"""
Used for manual data from 'data' directory
"""
import numpy as np
import pandas as pd
from sat import Sat, SatType
from params import Params, ReferenceOrbit

class SatReader:
    def __init__(self, ref_orbit: ReferenceOrbit, params: Params):
        self.ref_orbit = ref_orbit
        self.params = params
        self.sat_list = []
    
    def read_data(self, file_path: str) -> list[Sat]:
        df = pd.read_csv(file_path, sep=",")
        for _, row in df.iterrows():
            x = np.array([[row["x0"], row["y0"], row["z0"]]]).reshape(3, 1)
            v = np.array([[row["vx0"], row["vy0"], row["vz0"]]]).reshape(3, 1)
            sat_type = SatType.from_str(row["sat_type"])
            self.sat_list.append(Sat(x, v, sat_type, self.ref_orbit, self.params))
        return self.sat_list