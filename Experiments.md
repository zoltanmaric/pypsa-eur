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
%load_ext autoreload
%autoreload

n = pypsa.Network("results/networks/elec_s_all_ec_lv1.1_2H.nc")
# n = pypsa.Network("results/networks/elec_s_37_ec_lcopt_Co2L-3H.nc")
df = n.buses_t.p
q1 = np.quantile(df, 0.25)
q3 = np.quantile(df, 0.75)
print(q1)
print(q3)
iqr = q3 - q1
print()
print(iqr)
min = q1 - 1.5 * iqr
max = q3 + 1.5 * iqr
print()
print(min)
print(max)

df[min < df][df < max]


# fig = px.histogram(df)
# fig.update_layout(height=1000)
```

```python
import scripts.plot_power_flow as ppf
import plotly.express as px
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
