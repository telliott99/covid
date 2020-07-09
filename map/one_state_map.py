# python3
import sys, os, json

if sys.version_info[0] < 3:
    print('use python3 for this script')
    sys.exit()

base = os.environ.get('covid_base')
if not base in sys.path:
    sys.path.insert(0,base)
    sys.path.insert(1,base + '/myutil')

import udb, udates
import uinit, ukeys, umath, ucolors


if not len(sys.argv) > 1:
    print('please supply the name of a state')
    sys.exit()
    
path_to_db = base + '/db.txt'

# use long form internally
from ustates import abbrev_to_state as stD

states = []
for arg in sys.argv[1:]:
    if arg in stD:
        states.append(stD[arg])
    elif arg in stD.values():
        states.append(arg)
        
print(states)

date_info, D = udb.load_db(path_to_db)

#--------------------

# GeoJSON data for US counties

fn = base + '/map/map_data/counties.json'
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
        D,state, mode='state')
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
from ucolors import cL

fig = px.choropleth(
    df,
    geojson=counties,
    locations='fips',
    color='stat',
    color_continuous_scale=cL,
    scope="usa",
    labels={'color':'growth'})

fig.show()
