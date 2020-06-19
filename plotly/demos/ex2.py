import sys, os
base = os.environ.get('covid_base')

sys.path.insert(0,base)
sys.path.insert(1,base + '/myutil')
from ustrings import us_states
from umath import stat

from all_states import rL, labels

#------
us_states['DC'] = 'DC'
states = [us_states[e] for e in labels]
        
values = []
for vL in rL:
    st = stat(vL[-15:])
    values.append(st)

#---------------------

import plotly.express as px

fig = px.choropleth(
    locations = states,
    locationmode="USA-states", 
    color=values, 
    scope="usa")
    
fig.show()