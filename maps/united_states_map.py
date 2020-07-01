# python3
import sys, os, json

if sys.version_info[0] < 3:
    print('use python3 for this script')
    sys.exit()

base = os.environ.get('covid_base')
sys.path.insert(0,base)

import myutil.ustrings as ustrings
import myutil.udb as udb
import myutil.ukeys as ukeys
import myutil.umath as umath
   
#--------------------

# we need to construct a pandas data frame with
# fips stats

sys.path.insert(1,base + '/analysis')
# as Alabama, but contains 'DC'
from all_states import states, rL

#i = states.index('DC')
#states[i] = 'District of Columbia'

# dict from 'Alabama' to 'AL'
from ustates import states
from ustates import state_to_abbrev as stD

abbrev = [stD[state] for state in states]

st = [umath.stat(vL[-7:]) for vL in rL]

#--------------------

import pandas as pd

df = pd.DataFrame(data={'state':abbrev, 'value':st})

#--------------------

import plotly.express as px

cL = ['rgb(0,100,0)',
      'rgb(0,255,0)',
      'rgb(111,255,0)',
      'rgb(255,255,0)',
      'rgb(255,111,0)',
      'rgb(255,0,0)']

fig = px.choropleth(
    df,
    locations=abbrev,
    locationmode='USA-states',
    color=st,
    #color_continuous_scale=cL,
    color_continuous_scale='Plasma',
    scope="usa",
    labels={'color':'growth'})

fig.show()
