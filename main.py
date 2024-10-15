from params import Params, ReferenceOrbit
from sat import Sat
from right_function import get_f
from integ import pk_4
import numpy as np


par = Params()

ref = ReferenceOrbit(par, 0)

x0 = np.array([
    [0, 1, 1]
]).reshape(3,1)
v0 = np.array([
    [1,0,0]
]).reshape(3,1)
sat = Sat(x0, v0, 1, par)
print(sat)
upr = np.array([
    [0, 0, 0]
])

x1 = pk_4(np.append(x0.T, v0.T, axis=1), get_f, upr, par)
print(x1[0,:3].reshape(3,1))

# u = np.array([[0, 1, 1]])
# c = np.array([[2, -2, 2]])

# sat = Sat(u, c, 1)
# print(sat)
# sat.get_osk_to_iso(par.omega)
# print(sat.__dict__)
