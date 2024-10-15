from params.parametrs import Params
from sat import Sat
from integ import pk_4
import numpy as np


par = Params()

u = np.array([[0, 1, 1]])
c = np.array([[2, -2, 2]])

sat = Sat(u, c, 1)
print(sat)
sat.get_osk_to_iso(par.omega)
print(sat)