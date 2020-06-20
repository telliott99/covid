# python3
import json, csv
import pandas as pd

fn = 'counties.json'
with open(fn,'r') as fh:
    counties = json.load(fh)

fn = 'unemp.csv'
df = pd.read_csv(fn, dtype={'fips': str})

# ---------------------------------------

import plotly.express as px

fig = px.choropleth(df, 
          geojson=counties, 
          locations='fips', 
          color='unemp',
          color_continuous_scale="Plasma",
          range_color=(0, 12),
          scope="usa",
          labels={'unemp':'unemployment rate'})
          
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

