import numpy as np
import pandas as pd
from sat import Sat

class SatWriter:
    def __init__(self, sat_list: list[Sat]):
        self.sat_list = sat_list
    
    def write_sat(self):
        for i, sat in enumerate(self.sat_list):
            df = pd.DataFrame(sat.get_vector(0, "osk").T, columns =['x0', 'y0', 'z0', 'vx0', 'vy0', 'vz0'])
            df['sat_type'] = sat.sat_type
            df['sat_name'] = f'sat_{i}'
            if i == 0:
                df_merged = df
            else:
                df_merged = pd.concat([df_merged, df], ignore_index=True)
        df_merged.to_csv("data.csv", index=False, sep=',')