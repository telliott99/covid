import sys, os, subprocess

import scipy.signal as signal

base = os.environ.get('covid_base')
sys.path.insert(0,base)

import myutil.ustrings as ustrings
import myutil.udb as udb
import myutil.udates as udates
import myutil.ufile as ufile
import myutil.ufmt as ufmt
import myutil.uinit as uinit
import myutil.ukeys as ukeys
import myutil.umath as umath

#---------------------------------------

conf = uinit.clargs()
mode = conf['mode']
    
sep = ustrings.sep      # ;
path_to_db = base + '/db.max.txt'

date_info, D = udb.load_db(path_to_db)

first,last = date_info.split('\n')
conf['first'] = first
conf['last'] = last

#---------------------------------------

kL = ukeys.key_list_for_search_term(D,'US', mode="country")

rL = []
for k in kL:
    try:
        rL.append(D[k][conf['mode']])
    except:
        print('error with: %s' % k)
        
vL = umath.totals(rL)
pL = []

for x,y in zip(vL[:-1],vL[1:]):
    pL.append(y - x)


# smooth
f = signal.savgol_filter
#pL = f(pL,51,3)
    
#---------------------------------------

import plotly.graph_objects as go

plt_us = go.Scatter(
    x=list(range(len(pL))),
    y=pL,
    line={'color':'blue', 'width':3})
    
fig = go.Figure(plt_us)

from eu import do_eu
rL,ignore = do_eu()

vL = umath.totals(rL)
pL = []

for x,y in zip(vL[:-1],vL[1:]):
    pL.append(y - x)

# problem

print(pL)
print(pL[38])  # 17861
pL[38] = (pL[37] + pL[39])/2.0

print(pL[52])  # 628451
pL[52] = (pL[51] + pL[53])/2.0

# smooth
#pL = f(pL,51,3)

plt_eu = go.Scatter(
    x=list(range(len(pL))),
    y=pL,
    line={'color':'red', 'width':3})

fig.add_trace(plt_eu)

fig.update_layout(yaxis=dict(range=[0,50000]))

fig.show()


