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
%load_ext autoreload
%autoreload

# n = pypsa.Network("results/networks/elec_s_all_ec_lv1.0_2H.nc")

# droppables = (n.generators.T.filter(like='OCGT').columns.to_list() +
#     n.generators.T.filter(like='CCGT').columns.to_list() +
#     n.generators.T.filter(like='lignite').columns.to_list() +
#     n.generators.T.filter(like='nuclear').columns.to_list() +
#     n.generators.T.filter(like='coal').columns.to_list() +
#     n.generators.T.filter(like='oil').columns.to_list() +
#     n.generators.T.filter(like='biomass').columns.to_list())

# n.generators.drop(droppables).p_nom.sort_values(ascending=False).head(100)

n = pypsa.Network('networks/base.nc')
n.loads_t.p_set
# n.snapshots
# n.generators.T.filter(like='OCGT').columns.to_list()
```

```python
import scripts.plot_power_flow as ppf
%load_ext autoreload
%autoreload

# n = pypsa.Network("results/networks/elec_s_all_ec_lv1.1_2H.nc")
n = pypsa.Network("results/networks/elec_s_37_ec_lcopt_Co2L-3H.nc")
# n.generators_t.p[n.generators.query('bus=="1005"').index]
display(n.lines.head())
n.lines.apply(lambda line: [n.buses.loc[line.bus0].x, n.buses.loc[line.bus1].x, None], axis='columns').head()
# display(n.loads_t.p.head())
```

```python
import scripts.plot_power_flow as ppf
%load_ext autoreload
%autoreload

n = pypsa.Network("results/networks/elec_s_all_ec_lv1.1_2H.nc")
# n = pypsa.Network("results/networks/elec_s_37_ec_lcopt_Co2L-3H.nc")
# snapshots = n.snapshots[range(326*8, 333*8)]
# n.loads_t.p_set.filter(['AL1 0']).loc[snapshots]
fig = ppf.colored_network_figure(n)
fig.update_layout(height=1300)
fig
```
