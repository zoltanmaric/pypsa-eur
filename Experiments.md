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
import cartopy.crs as ccrs
plt.style.use("bmh")
%matplotlib inline

n = pypsa.Network("networks/elec.nc")
# n.plot()

fig,ax = plt.subplots(
    figsize=(30,30),
    subplot_kw={"projection": ccrs.PlateCarree()}
)

n.plot(ax=ax, boundaries=(5.5, 15.5, 47, 55))

ax.axis('off')
```

```python
import plotly.graph_objects as go

n.iplot()
"bro"
```

```python
import pandas as pd
pd.options.display.max_columns = None # show all columns of a dataframe
pd.options.display.max_rows = None # show all rows of a dataframe

n.generators.query('carrier == "solar"').head()
```

```python
display(n.generators.query('p_nom_extendable == True and carrier not in ["onwind", "offwind", "offwind-ac", "offwind-dc", "solar"]').head())
n.buses.loc[['4931']]
```
