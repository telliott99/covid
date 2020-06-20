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
    if st > 0.03:
        values.append('2')
    elif st > 0.02:
        values.append('1')
    else:
        values.append('0')
    
#---------------------

import plotly.express as px
cL = ['salmon','red',"rgb(195, 195, 195)"]

fig = px.choropleth(
    locations = states,
    locationmode="USA-states",
    color=values,
    color_discrete_sequence=cL, 
    scope="usa")

print(fig)

fig.show()