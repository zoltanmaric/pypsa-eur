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
generators = n.generators.query('carrier.str.contains("wind")')
display(generators.head())
renamed = n.generators_t.p.filter(like='wind').rename(generators.bus, axis='columns').rename_axis('Bus', axis='columns')
print('renamed')
display(renamed.head())
print('grouped')
renamed.groupby(by=lambda x: x, axis='columns').sum().head()
# display(n.loads_t.p.head())
```

```python
import scripts.plot_power_flow as ppf
%load_ext autoreload
%autoreload

# n = pypsa.Network("results/networks/elec_s_all_ec_lv1.1_2H.nc")
n = pypsa.Network("results/networks/elec_s_37_ec_lcopt_Co2L-3H.nc")
# snapshots = n.snapshots[range(326*8, 333*8)]
# n.loads_t.p_set.filter(['AL1 0']).loc[snapshots]
fig = ppf.colored_network_figure(n)
fig.update_layout(height=1300)
fig
```

```python
import pypsa
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
plt.style.use("bmh")
%matplotlib inline

n = pypsa.Network("networks/elec.nc")
# n.plot()

fig,ax = plt.subplots(
    figsize=(10,10),
    subplot_kw={"projection": ccrs.PlateCarree()}
)

n.plot(ax=ax, boundaries=(-9, 28, 30, 75))

ax.axis('off')
```

```python
import sys
sys.path.append('/Users/zoltan/github/PyPSA')
import pypsa
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
plt.style.use("bmh")
%matplotlib inline

n = pypsa.Network("results/networks/elec_s_37_ec_lcopt_Co2L-3H.nc")

n.iplot(
    mapbox=True,
    size=(2000, 2000)
)
```

```python
#display(n.components)
display(n.buses_t.marginal_price.iloc[0].head())
display(n.lines.head())
```
