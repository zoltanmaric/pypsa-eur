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

```python
import scripts.plot_power_flow as ppf
import numpy as np
import pypsa
%load_ext autoreload
%autoreload

n = pypsa.Network("results/networks/elec_s_all_ec_lv1.1_2H.nc")
# display(n.buses.loc[n.lines.bus0].x)
# display(n.buses.loc[n.lines.bus0].y)

# display(n.buses.loc[n.lines.bus1].x)
# display(n.buses.loc[n.lines.bus1].y)
display(n.lines.head())
n.lines_t.p0.head()
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
%load_ext autoreload
%autoreload

n = pypsa.Network("results/networks/elec_s_all_ec_lv1.1_2H.nc")
# n = pypsa.Network("results/networks/elec_s_37_ec_lcopt_Co2L-3H.nc")
# snapshots = n.snapshots[range(326*8, 333*8)]
# n.loads_t.p_set.filter(['AL1 0']).loc[snapshots]
# fig = ppf.colored_network_figure(n, n.buses_t.p)
fig = ppf.colored_network_figure(n, 'generation', technology='solar')
fig.update_layout(height=1000)
fig
```
