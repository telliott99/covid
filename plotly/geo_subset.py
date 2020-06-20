import sys, os, json
import pandas as pd

base = os.environ.get('covid_base')
sys.path.insert(0,base)

import myutil.states_fips as sf
import myutil.udb as udb
import myutil.ukeys as ukeys
import myutil.umath as umath

#------------------------

# GeoJSON data:

fn = 'counties.json'
with open(fn,'r') as fh:
    counties = json.load(fh)

#------------------------

# dict of state abbrev to fips

fD = sf.get_fips_dict()
    
#------------------------

def features_for_state(abbrev):
    fips = fD[abbrev]
    sL = counties['features']
    sL = [e for e in sL if e[u'properties'][u'STATE'] == fips]
    return sL
    
state = 'SC'
    
features = features_for_state('SC')

# reassemble FeatureCollection

geo = {'type':'FeatureCollection'}
geo['features'] = features
print(geo)

#------------------------


#------------------------

import plotly.express as px

fig = px.choropleth(
          geojson=geo,
          scope="usa")
          
fig.show()
print(fig)
