import pandas as pd
import numpy as np
from sat import Sat
from params import Params, ReferenceOrbit

params = Params()

# Time period
dt = 1
T = 2 * np.pi / params.omega
t = np.arange(dt, 2*T, dt)

# Reference Orbit
reference_orbit = ReferenceOrbit(params, dt)

df = pd.read_csv('data.csv')
for index, row in df.iterrows():
    print(index)
    print(row["x0"])
    x = np.array([[row["x0"], row["y0"], row["z0"]]]).reshape(3, 1)
    v = np.array([[row["vx0"], row["vy0"], row["vz0"]]]).reshape(3, 1)
    sat_type = row["sat_type"]
    print(Sat(x,v,sat_type,reference_orbit,params))