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

conf = uinit.clargs()
if not conf['arg']:
    print('please supply the name of a state')
    sys.exit()
    
state = conf['arg']

date_info, D = udb.load_db()

#--------------------

# GeoJSON data for US counties

fn = '../data/counties.json'
with open(fn,'r') as fh:
    counties = json.load(fh)
    
# we do not need to filter:
# sL = counties['features']
# sL = [e for e in sL if e[u'properties'][u'STATE'] == fips]
   
#--------------------

# we need to construct a pandas data frame with
# fips stats

state = state

kL = ukeys.key_list_for_search_term(
    state, mode='state')

rL = [D[k]['cases'][-10:] for k in kL]
sL = [umath.stat(vL) for vL in rL]

#--------------------

fips = [ukeys.fips_for_key(k) for k in kL]

#--------------------

import pandas as pd

df = pd.DataFrame(
    {
     'fips':fips,
     'stat':sL
    })

print(df)

#--------------------

import plotly.express as px

#scale = px.colors.sequential.Plasma[3:]
cL = ['rgb(0,100,0)',
      'rgb(0,255,0)',
      'rgb(111,255,0)',
      'rgb(255,255,0)',
      'rgb(255,111,0)',
      'rgb(255,0,0)']

fig = px.choropleth(
    df,
    geojson=counties,
    locations='fips',
    color='stat',
    color_continuous_scale=cL,
    scope="usa",
    labels={'color':'growth'})

fig.show()
