import sys, os
base = os.environ.get('covid_base')

sys.path.insert(0,base)
sys.path.insert(1,base + '/myutil')

import udb, ukeys
from umath import stat

date_info, D = udb.load_db()

kL = ukeys.key_list_for_us_counties()

rL = [D[k]['cases'] for k in kL]
values = [] 
for vL in rL:
    st = stat(vL[-15:])
    if st > 0.04:
        values.append(4)
    elif st > 0.03:
        values.append(3)
    elif st > 0.02:
        values.append(2)
    else:
        values.append(1)

cL = [ukeys.fips_for_key(k) for k in kL]

#---------------------

import plotly.express as px
import json

import pandas as pd

fn = 'data/counties.json'
with open(fn,'r') as fh:
    geo = json.load(fh)

mD = { 'fips':cL, 'data':values }
df = pd.DataFrame.from_dict(mD)
    
fig = px.choropleth(
    df,
    geojson=geo,
    locations='fips',
    color='data', 
    #locationmode="USA-states", 
    scope="usa")
    
fig.show()


