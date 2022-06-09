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
    figsize=(10,10),
    subplot_kw={"projection": ccrs.PlateCarree()}
)

n.plot(ax=ax, boundaries=(5.5, 15.5, 47, 55))

ax.axis('off')
```

```python
#display(n.components)
display(n.buses.head())
display(n.lines.head())
```

```python
line0 = n.lines.iloc[0]
display(line0.bus0, line0.bus1)
display(n.buses.loc[line0.bus0].x)
n.buses.v_nom.to_list()[:10]
```

```python
import plotly.graph_objects as go
import plotly.express as px


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
for name, bus in n.buses.iterrows():
    x, y = bus.x, bus.y
    node_x.append(x)
    node_y.append(y)

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
node_trace.marker.color = n.buses.v_nom.to_list()
node_trace.text = n.buses.index.to_list()


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
fig = go.Figure(go.Scattergeo())
fig.update_geos(scope="europe", center=dict(lat=54, lon=10), lataxis_range=[47,60], lonaxis_range=[0, 20])
fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
```

```python
import plotly.express as px

fig = px.line_geo(lat=[0,15,20,35], lon=[5,10,25,30])
fig.update_geos(fitbounds="locations")
fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
```

```python
n.iplot(size=(1000,1000))
"bro"
```

```python
import pandas as pd
pd.options.display.max_columns = None # show all columns of a dataframe
pd.options.display.max_rows = None # show all rows of a dataframe

n.generators.query('Generator in ["3370 solar"]').head()
```

```python
display(n.generators.query('p_nom_extendable == True and carrier not in ["onwind", "offwind", "offwind-ac", "offwind-dc", "solar"]').head())
n.buses.loc[['4931']]
```
