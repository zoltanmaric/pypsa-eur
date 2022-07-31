import pypsa
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
plt.style.use("bmh")

n = pypsa.Network("networks/elec.nc")

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/scripts'
print(f'currentdir: {currentdir}')
sys.path.insert(0, currentdir)

import solve_network

n = solve_network.prepare_network(n, {"load_shedding": True})
n.lopf(
        n.snapshots[0:2],
        solver_name="cbc",
        pyomo=False,
    )
