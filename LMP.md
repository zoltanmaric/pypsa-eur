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
import geopandas as gpd
import matplotlib.pyplot as plt
%matplotlib inline
europe = gpd.read_file('resources/europe_shape.geojson')
europe.plot()
```

```python
# Without GB, NO, SE, FI, LV, LT, EE
europe = gpd.read_file('resources/europe_shape.geojson')
europe.plot()
```

```python
# The above plus GB
europe = gpd.read_file('resources/europe_shape.geojson')
europe.plot()
```

```python
# The above minus IE and GB
europe = gpd.read_file('resources/europe_shape.geojson')
europe.plot()
```

```python
import pypsa
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
plt.style.use("bmh")
%matplotlib inline

n = pypsa.Network("results/networks/elec_s_128_ec_lcopt_2H.nc")
# n.plot()

fig,ax = plt.subplots(
    figsize=(30,30),
    subplot_kw={"projection": ccrs.PlateCarree()}
)

max_marginal_price = n.buses_t.marginal_price.max().max()
min_marginal_price = n.buses_t.marginal_price.min().min()
colors = (n.buses_t.marginal_price.loc[n.snapshots[6]] - min_marginal_price) / (max_marginal_price - min_marginal_price)

display(n.buses_t.marginal_price)
n.plot(ax=ax, bus_colors=colors, bus_cmap=plt.cm.jet)
# n.plot(ax=ax, boundaries=(-9, 28, 30, 75))

ax.axis('off')
```

```python
n = pypsa.Network("results/networks/elec_s_143_ec_lcopt_2H.nc")
display(n.buses_t.marginal_price)

for snapshot in n.snapshots[0:1]:
    display(snapshot)
    prices = bus_text=n.buses_t.marginal_price.loc[snapshot]
    n.iplot(
        mapbox=True,
        size=(2000, 2000),
        bus_text=prices,
        bus_colors=prices,
        line_text=None
    )
```

```python
n.lopf(
        n.snapshots[0:2],
        solver_name="cbc",
        pyomo=False,
    )
```
