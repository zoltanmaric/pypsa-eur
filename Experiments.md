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
import plotly.express as px


# n = pypsa.Network("results/networks/elec_s_37_ec_lcopt_Co2L-3H.nc")
n = pypsa.Network("results/networks/elec_s_all_ec_lv1.0_2H.nc")


# Create edges
edge_x = []
edge_y = []
for name, line in n.lines.iterrows():
    bus0 = n.buses.loc[line.bus0]
    bus1 = n.buses.loc[line.bus1]
    x0, y0 = bus0.x, bus0.y
    x1, y1 = bus1.x, bus1.y
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scattermapbox(
    lon=edge_x, lat=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
index = 6
snapshot = n.snapshots[index]
marginal_prices = []
for name, bus in n.buses.iterrows():
    marginal_price = n.buses_t.marginal_price.loc[snapshot][name]
    if marginal_price > -650 and marginal_price < 0:
        x, y = bus.x, bus.y
        node_x.append(x)
        node_y.append(y)
        marginal_prices.append(marginal_price)

node_trace = go.Scattermapbox(
    lon=node_x, lat=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        )))

# Color nodes
display(snapshot)
node_trace.marker.color = marginal_prices
node_trace.text = marginal_prices


#Create Network Graph
fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0}, mapbox_style="open-street-map")
fig.show()

```

```python
import pandas as pd
import sys
import pypsa
pd.options.display.max_columns = None # show all columns of a dataframe
pd.options.display.max_rows = 50 # show 50 rows of a dataframe


n = pypsa.Network("networks/elec_s_all_ec_lv1.0_2H.nc")
# n = pypsa.Network("networks/elec_s_37_ec_lcopt_Co2L-3H.nc")

display(n.generators.query("p_nom_extendable"))
display(n.storage_units.query("p_nom_extendable"))
n.stores.query("e_nom_extendable")
```
