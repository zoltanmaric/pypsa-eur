---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.8
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

```python
import pypsa
import matplotlib.pyplot as plt
plt.style.use("bmh")
%matplotlib inline

n = pypsa.Network("results/networks/elec_s_6_ec_lcopt_Co2L-24H.nc")
n.plot()
```

```python
for c in n.iterate_components(list(n.components.keys())[2:]):
    print(f"Component '{c.name}' has {len(c.df)} entries")
```

```python
len(n.snapshots)
```

```python
n.lines
```

```python
n.generators
```

```python
n.loads_t.p_set.plot(figsize=(15,3))
```

```python
n.generators_t.p_max_pu.groupby(lambda col: col[:5], axis=1).sum().plot(figsize=(15,3))
```

```python
n.objective / 1e9 # billion euros p.a.
```

```python
n.lines_t.p0
```

```python
(n.lines.s_nom_opt - n.lines.s_nom) # Transmission line expansion
```

```python
# Optimal Generator/Storage Capacities
n.generators.groupby("carrier").p_nom_opt.sum() / 1000 #GW
```

```python
# Storage units are not listed under extandable carriers in config.yaml
n.storage_units
```

```python
import pandas as pd
pd.options.display.max_columns = None # show all columns of a dataframe
n.stores
```

```python
# Plot solution (grid and generators)
import cartopy.crs as ccrs
loading = (n.lines_t.p0.abs().mean().sort_index() / (n.lines.s_nom_opt*n.lines.s_max_pu).sort_index()).fillna(0.)
loading
```

```python
fig,ax = plt.subplots(
    figsize=(10,10),
    subplot_kw={"projection": ccrs.PlateCarree()}
)

n.plot(ax=ax,
       bus_colors='gray',
       branch_components=["Line"],
       line_widths=n.lines.s_nom_opt/3e3,
       line_colors=loading,
       line_cmap=plt.cm.viridis,
       color_geomap=True,
       bus_sizes=0,
       boundaries=(5.5, 15.5, 47, 55))

ax.axis('off')
```
