# this works
# use this to test if/when things stop working

import sys, os, json

base = os.environ.get('covid_base')
fn = base + '/plotly/data/counties.json'
with open(fn,'r') as fh:
    counties = json.load(fh)

#-------------------------------

# still working on how to do this w/o pandas

import pandas as pd

# note:  dtype required for map to display correctly
df = pd.read_csv('example.csv', dtype={'fips': str})
print (df.head())

'''
    fips  value
0  01001      1
1  06071      2
'''

# largest county in the US:  San Bernardino, CA

#-------------------------------
    
import plotly.express as px

cL = ['green','magenta']

fig = px.choropleth(
    df,
    geojson=counties,
    locations='fips',
    color=["Autauga","San Bernardino"],
    color_discrete_sequence=cL,
    scope='usa')
    
fig.show()

'''
county ids are really fips by another name
px uses 'fips' as the key into the data frame
to retrieve the value in the 'value' column

w/o scope, it draws the whole world
'''