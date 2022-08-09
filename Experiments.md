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
#display(n.components)
display(n.buses_t.marginal_price.iloc[0].head())
display(n.lines.head())
```

```python
import plotly.graph_objects as go
import numpy as np

# Create figure
fig = go.Figure()

# Add traces, one for each slider step
for step in np.arange(0, 5, 0.1):
    fig.add_trace(
        go.Scatter(
            visible=False,
            line=dict(color="#00CED1", width=6),
            name="𝜈 = " + str(step),
            x=np.arange(0, 10, 0.01),
            y=np.sin(step * np.arange(0, 10, 0.01))))

# Make 10th trace visible
fig.data[10].visible = True

# Create and add slider
steps = []
for i in range(len(fig.data)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
              {"title": "Slider switched to step: " + str(i)}],  # layout attribute
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)
    
display(steps[0])

slider = dict(
    active=10,
    currentvalue={"prefix": "Frequency: "},
    pad={"t": 50},
    steps=steps
)

fig.update_layout(
    sliders=[slider]
)

fig.show()
```

```python
import scripts.plot_power_flow as ppf

n = pypsa.Network("results/networks/elec_s_all_ec_lv1.0_2H.nc")
ppf.colored_network_figure(n)
```

```python
import pandas as pd
import sys
import pypsa
pd.options.display.max_columns = None # show all columns of a dataframe
pd.options.display.max_rows = 100 # show 50 rows of a dataframe


n = pypsa.Network("results/networks/elec_s_all_ec_lv1.0_2H.nc")
# n = pypsa.Network("networks/elec_s_37_ec_lcopt_Co2L-3H.nc")

# display(n.generators_t)
# generators_t = pd.concat([n.generators_t[k]['1004 onwind'] for k in n.generators_t.keys() if not n.generators_t[k].empty])
# display(n.solutions)
display(n.generators_t.p / (n.generators_t.p_max_pu * n.generators.p_nom) * 100)
# display(n.generators_t.p[n.generators_t.p_max_pu * n.generators.p_nom > n.generators_t.p])

# for k in n.generators_t.keys():
#     print(k)
#     display(n.generators_t[k])


# index = 6
# snapshot = n.snapshots[index]

# display(n.generators)
# # display(n.generators_t.p)
# display(n.generators_t.keys())

# n.generators_t.p_set.loc[snapshot][[n.generators_t.p_set.loc[snapshot] < n.generators.p_max_pu * n.generators.p_nom]]
# generators_t.query("p_nom * p_max_pu > p_set")
# display(n.storage_units.query("p_nom_extendable"))
# n.stores.query("e_nom_extendable")
```
