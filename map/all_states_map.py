# python3
import sys, os, json

if sys.version_info[0] < 3:
    print('use python3 for this script')
    sys.exit()

base = os.environ.get('covid_base')
if not base in sys.path:
    sys.path.insert(0,base)
    sys.path.insert(1,base + '/myutil')

import udb, ukeys, umath, ucolors
   
#--------------------

# we need to construct a pandas data frame with
# fips stats

sys.path.insert(1,base + '/analysis')

from all_states import states, rL

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

from ucolors import cL

fig = px.choropleth(
    df,
    locations=abbrev,
    locationmode='USA-states',
    color=st,
    color_continuous_scale=cL,
    scope="usa",
    labels={'color':'growth'})

fig.show()
