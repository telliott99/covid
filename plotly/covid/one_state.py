# python3
import sys, os, json

base = os.environ.get('covid_base')
sys.path.insert(0,base)

import myutil.ustrings as ustrings
import myutil.udb as udb
import myutil.udates as udates
import myutil.ukeys as ukeys

#--------------------

# GeoJSON data for US counties

fn = '../data/counties.json'
with open(fn,'r') as fh:
    counties = json.load(fh)
    
# we do not need to do this:
# sL = counties['features']
# sL = [e for e in sL if e[u'properties'][u'STATE'] == fips]
   
#--------------------

# we need to construct a pandas data frame with
# fips stats

state = "South Carolina"
kL = ukeys.key_list_for_search_term(state,mode="state")

# dict from 'AL' to '01'
from myutil.states_fips import get_fips_dict
fD = get_fips_dict()



abbrev = [us_states[state] for state in states]
fips = [fD[e] for e in abbrevs]

for st, vL in zip(abbrev,rL):
    print(st, vL[-1])

df = pd.DataFrame({'state':abbrev, 'fips':fips} )

sys.exit()


#--------------------

import plotly.express as px

fig = px.choropleth(
    geojson=counties,
    scope="usa")

fig.show()
