# python3
import sys, os, json

base = os.environ.get('covid_base')
sys.path.insert(0,base)

import myutil.ustrings as ustrings
import myutil.udb as udb
import myutil.udates as udates
import myutil.uinit as uinit
import myutil.ukeys as ukeys
import myutil.umath as umath


if not len(sys.argv) > 1:
    print('please supply the name of a state')
    sys.exit()

# use long form internally
from ustrings import abbrev_to_state as stD

states = []
for arg in sys.argv[1:]:
    if arg in stD:
        states.append(stD[arg])
    elif arg in stD.values():
        states.append(arg)
        
print(states)

date_info, D = udb.load_db()

#--------------------

# GeoJSON data for US counties

fn = base + '/data_geo/counties.json'
with open(fn,'r') as fh:
    counties = json.load(fh)
    
# we do not need to filter:
# sL = counties['features']
# sL = [e for e in sL if e[u'properties'][u'STATE'] == fips]
   
#--------------------

# we need to construct a pandas data frame with
# fips stats

kL = []
for state in states:
    skL = ukeys.key_list_for_search_term(
        state, mode='state')
    kL.extend(skL)

rL = [D[k]['cases'][-10:] for k in kL]
sL = [umath.stat(vL) for vL in rL]

sL = [umath.quintiles(n) for n in sL]

#--------------------

fips = [ukeys.fips_for_key(k) for k in kL]

#--------------------

import pandas as pd

df = pd.DataFrame(
    {
     'fips':fips,
     'stat':sL
    })

#print(df)

#--------------------

import plotly.express as px
from colors import cL

fig = px.choropleth(
    df,
    geojson=counties,
    locations='fips',
    color='stat',
    color_continuous_scale=cL,
    scope="usa",
    labels={'color':'growth'})

fig.show()
