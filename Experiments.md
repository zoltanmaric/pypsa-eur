---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.0
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Buses

```python
import scripts.plot_power_flow as ppf
import numpy as np
import pypsa
%load_ext autoreload
%autoreload

n = pypsa.Network("results/networks/elec_s_all_ec_lv1.01_2H.nc")
display(n.buses.loc['4977'])
# display(n.buses_t.p.head())
display(n.buses_t.p.iloc[6]["4977"])
display(n.buses_t.keys())
```

# Generators

```python
display(n.generators.columns)
display(n.generators.query('bus=="4977"'))
display(n.generators.query('bus=="4977"')[['p_nom', 'p_nom_opt', 'p_max_pu', 'marginal_cost']])
display(n.generators_t.keys())

import pandas as pd
p = n.generators_t.p.iloc[6].rename('p')
q = n.generators_t.q.iloc[6].rename('q')
p_set = n.generators_t.p_set.iloc[6].rename('p_set')
p_max_pu = n.generators_t.p_max_pu.iloc[6].rename('p_max_pu')
generators_t = pd.concat([p, q, p_set, p_max_pu], axis='columns')

generators = n.generators[['p_nom_opt', 'bus', 'carrier']].join(generators_t)\
    .rename({'bus': 'Bus'}, axis='columns')\
    .set_index(['Bus', 'carrier'])\
    .rename_axis('quantities', axis='columns')
print('generators flattened')
display(generators.query('Bus=="4977"').head())

print('generators unstacked')
generators_unstacked = generators.unstack()\
    .reorder_levels(['carrier', 'quantities'], axis='columns')\
    .sort_index(axis=1)
# generators_unstacked = generators.unstack().swaplevel(axis='columns').sort_index(axis=1)
display(generators_unstacked.head())
display(generators_unstacked.iloc[0]['solar'])
```

# Stores

```python
bus = '1208'
display(n.storage_units.query('bus==@bus'))
mask = n.storage_units_t.p.iloc[0].index.str.startswith(bus)
n.storage_units_t.p.iloc[0][mask].to_frame()
```

# Loads

```python
display(n.loads.query('bus=="4977"').head())
display(n.loads_t.keys())
display(n.loads_t.p.head())
display(n.loads_t.p.iloc[6]['4977'])
display(pd.DataFrame(n.loads_t.p.iloc[0].rename('p')).rename_axis('Bus', axis='index').head())
```

# Lines & Links

```python
# display(n.lines.query('bus0=="4977" or bus1=="4977" or bus0=="4983" or bus1=="4983"'))
line = n.lines.loc['11274']
display(line)
display(line.geometry)
print()
print('bus0')
display(n.buses.loc[line.bus0])
print()
print('bus1')
display(n.buses.loc[line.bus1])
# bus_name = 'bus0'
# display(n.lines[bus_name].head())
# n.buses.loc[n.lines[bus_name]][['x', 'y']].head()
```

# Components

```python
n.components['Generator']
```

```python
import scripts.plot_power_flow as ppf
import plotly.express as px
import pypsa
%load_ext autoreload
%autoreload

n = pypsa.Network("results/networks/elec_s_all_ec_lv1.1_2H.nc")
# n = pypsa.Network("results/networks/elec_s_37_ec_lcopt_Co2L-3H.nc")
df = n.buses_t.p.iloc[0]
fig = px.histogram(df[(-500 < df)][(df < 500)])
fig.update_layout(height=1000)
```

```python
import scripts.plot_power_flow as ppf
import pypsa
import plotly.graph_objects as go
%load_ext autoreload
%autoreload

n = pypsa.Network("results/networks/elec_s_all_ec_lv1.01_2H.nc")
# n = pypsa.Network("results/networks/elec_s_37_ec_lcopt_Co2L-3H.nc")
fig = ppf.colored_network_figure(n, 'net_power')
fig.update_layout(height=1000, mapbox=dict(center=go.layout.mapbox.Center(lat=55, lon=12), zoom=3.3))
fig
```
